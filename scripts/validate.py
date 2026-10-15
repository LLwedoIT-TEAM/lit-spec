"""Validate the normative schemas and every example LIT bundle."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


ROOT = Path(__file__).resolve().parents[1]
MANIFEST_NAMES = ("project", "components", "canon", "provenance", "rights")


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def duplicates(values: list[str]) -> set[str]:
    seen: set[str] = set()
    return {value for value in values if value in seen or seen.add(value)}


def validate() -> list[str]:
    errors: list[str] = []
    checker = FormatChecker()
    schemas: dict[str, Any] = {}

    for name in MANIFEST_NAMES:
        path = ROOT / "schema" / f"{name}.schema.json"
        schema = load_json(path)
        Draft202012Validator.check_schema(schema)
        schemas[name] = schema

    example_root = ROOT / "examples"
    example_dirs = sorted(path for path in example_root.iterdir() if path.is_dir())
    if not example_dirs:
        errors.append("examples: no example bundles found")

    for example in example_dirs:
        documents: dict[str, Any] = {}

        for name in MANIFEST_NAMES:
            path = example / f"{name}.json"
            if not path.is_file():
                errors.append(f"{path.relative_to(ROOT)}: required manifest is missing")
                continue

            document = load_json(path)
            documents[name] = document
            validator = Draft202012Validator(schemas[name], format_checker=checker)
            for error in sorted(
                validator.iter_errors(document), key=lambda item: list(item.absolute_path)
            ):
                location = "/".join(map(str, error.absolute_path)) or "<root>"
                errors.append(f"{path.relative_to(ROOT)}:{location}: {error.message}")

        if set(documents) != set(MANIFEST_NAMES):
            continue

        versions = {documents[name]["litVersion"] for name in MANIFEST_NAMES}
        if len(versions) != 1:
            errors.append(f"{example.relative_to(ROOT)}: inconsistent litVersion values")

        project_id = documents["project"]["id"]
        for name in MANIFEST_NAMES[1:]:
            if documents[name]["project"] != project_id:
                errors.append(
                    f"{example.relative_to(ROOT)}/{name}.json: project reference mismatch"
                )

        contributors = {item["id"] for item in documents["project"]["contributors"]}
        components = documents["components"]["components"]
        component_ids = [item["id"] for item in components]
        component_set = set(component_ids)
        for duplicate in sorted(duplicates(component_ids)):
            errors.append(f"{example.relative_to(ROOT)}: duplicate component ID {duplicate}")

        sequences = [item["sequence"] for item in components if "sequence" in item]
        for duplicate in sorted(duplicates([str(value) for value in sequences])):
            errors.append(f"{example.relative_to(ROOT)}: duplicate sequence {duplicate}")

        for component in components:
            unknown = set(component.get("contributors", [])) - contributors
            if unknown:
                errors.append(
                    f"{example.relative_to(ROOT)}: component {component['id']} has "
                    f"unknown contributors {sorted(unknown)}"
                )

        for relationship in documents["components"].get("relationships", []):
            for field in ("source", "target"):
                if relationship[field] not in component_set:
                    errors.append(
                        f"{example.relative_to(ROOT)}: relationship {field} "
                        f"{relationship[field]} is not a component"
                    )

        agents = documents["provenance"]["agents"]
        agent_ids = [item["id"] for item in agents]
        agent_set = set(agent_ids)
        for duplicate in sorted(duplicates(agent_ids)):
            errors.append(f"{example.relative_to(ROOT)}: duplicate agent ID {duplicate}")
        for activity in documents["provenance"]["activities"]:
            unknown = set(activity["agentIds"]) - agent_set
            if unknown:
                errors.append(
                    f"{example.relative_to(ROOT)}: activity {activity['id']} has "
                    f"unknown agents {sorted(unknown)}"
                )

        holders = documents["rights"]["holders"]
        holder_ids = [item["id"] for item in holders]
        holder_set = set(holder_ids)
        for duplicate in sorted(duplicates(holder_ids)):
            errors.append(f"{example.relative_to(ROOT)}: duplicate holder ID {duplicate}")

        covered_assets: set[str] = set()
        for grant in documents["rights"]["grants"]:
            if grant["holder"] not in holder_set:
                errors.append(
                    f"{example.relative_to(ROOT)}: grant {grant['id']} has unknown "
                    f"holder {grant['holder']}"
                )
            unknown = set(grant["assets"]) - component_set
            if unknown:
                errors.append(
                    f"{example.relative_to(ROOT)}: grant {grant['id']} has unknown "
                    f"assets {sorted(unknown)}"
                )
            covered_assets.update(grant["assets"])

        uncovered = component_set - covered_assets
        if uncovered:
            errors.append(
                f"{example.relative_to(ROOT)}: components without a rights grant "
                f"{sorted(uncovered)}"
            )

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validated 5 schemas and all example bundles; cross-reference checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
