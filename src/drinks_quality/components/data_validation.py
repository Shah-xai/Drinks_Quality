from pathlib import Path

import pandas as pd
import pandera as pa
from pandera import DataFrameSchema, Column, Check
import yaml

from drinks_quality import logger
from drinks_quality.entity.config_entity import DataValidationConfig


class DataValidation:
    def __init__(self, config: DataValidationConfig):
        self.config = config
        self.schema_dict = config.schema  # dict loaded from schema.yaml

    def run_validation(self) -> bool:
        # Load data
        df = pd.read_csv(self.config.data_file)

        # Build pandera schema from yaml dict
        schema = self._make_schema()

        ok = True
        failure_cases = []

        try:
            schema.validate(df, lazy=True)
            logger.info(" Data validation passed.")
        except pa.errors.SchemaErrors as e:
            ok = False
            logger.error(" Data validation failed.")
            # Turn failure cases into JSON/YAML-friendly objects
            failure_cases = e.failure_cases.to_dict(orient="records")

        # Always write report
        self._write_report(df, ok, failure_cases)
        return ok

    def _make_schema(self) -> DataFrameSchema:
        features = self.schema_dict["features"]
        target = self.schema_dict["target"]
        constraints = self.schema_dict.get("constraints", {})

        cols = {}

        # feature columns
        for name, rules in features.items():
            cols[name] = self._col(rules)

        # target column
        cols[target["name"]] = self._col(target)

        checks = []

        # max missing % per column
        max_missing = constraints.get("max_missing_percentage_per_column")
        if max_missing is not None:
            limit = float(max_missing)

            def missing_ok(df: pd.DataFrame) -> bool:
                return bool(((df.isna().mean() * 100) <= limit).all())

            checks.append(Check(missing_ok, element_wise=False))

        allow_extra = bool(constraints.get("allow_extra_columns", True))

        return DataFrameSchema(cols, checks=checks, strict=not allow_extra, coerce=True)

    def _col(self, rules: dict) -> Column:
        dtype = str(rules.get("dtype", "float")).lower()
        nullable = bool(rules.get("nullable", True))

        pa_type = pa.Int64 if dtype == "int" else pa.Float64

        checks = []
        if "min" in rules and "max" in rules:
            checks.append(Check.in_range(float(rules["min"]), float(rules["max"])))
        else:
            if "min" in rules:
                checks.append(Check.ge(float(rules["min"])))
            if "max" in rules:
                checks.append(Check.le(float(rules["max"])))

        if "allowed_values" in rules:
            checks.append(Check.isin(list(rules["allowed_values"])))

        return Column(pa_type, checks=checks, nullable=nullable)

    def _write_report(self, df: pd.DataFrame, ok: bool, failure_cases: list) -> None:
        report_path = Path(self.config.report_file_path)
        report_path.parent.mkdir(parents=True, exist_ok=True)

        missing_pct = (df.isna().mean() * 100).round(2).to_dict()

        report = {
            "status": "PASSED" if ok else "FAILED",
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "missing_percentage": missing_pct,
            "num_failure_cases": len(failure_cases),
            "failure_cases": failure_cases[:200],  # cap so report doesn't explode
        }

        with open(report_path, "w", encoding="utf-8") as f:
            yaml.safe_dump(report, f, sort_keys=False)

        logger.info(f"Validation report written to: {report_path}")
