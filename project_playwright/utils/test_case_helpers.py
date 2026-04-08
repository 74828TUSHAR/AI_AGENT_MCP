import traceback


def get_exception_line():
    return traceback.extract_tb(traceback.sys.exc_info()[2])[-1].lineno


def log_test_header(logger, test_name, scenarios):
    logger.info("\n" + "=" * 70)
    logger.info(f"TEST: {test_name}")
    logger.info("Scenarios:")
    for scenario_id, description in scenarios.items():
        logger.info(f"  {scenario_id.split('_')[1]} - {description}")
    logger.info("=" * 70 + "\n")


def mask_value(value):
    return "*" * len(str(value))
