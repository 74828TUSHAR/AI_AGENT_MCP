from utils.api_assertions import write_api_failure_artifact
from utils.test_case_helpers import get_exception_line, log_test_header


async def run_api_scenario(logger, test_case_name, scenario_name, scenario_callable):
    try:
        await scenario_callable()
        logger.info("%s passed", scenario_name.replace("_", " ").title())
    except Exception as exc:
        line_num = get_exception_line()
        logger.error("%s failed at line %s: %s", scenario_name.replace("_", " ").title(), line_num, exc)

        response = getattr(exc, "api_response", None)
        if response:
            artifact_path = write_api_failure_artifact(test_case_name, scenario_name, response)
            logger.error("API failure artifact saved: %s", artifact_path)

        raise AssertionError(f"{scenario_name} failed at line {line_num}: {exc}") from exc


def log_api_header(logger, test_name, scenarios):
    log_test_header(logger, test_name, scenarios)
