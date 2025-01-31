import yaml
import ray
import os

from ray.autoscaler._private.commands import prepare_config, validate_config
from ray.tests.aws.utils.constants import DEFAULT_CLUSTER_NAME
from ray.autoscaler._private.aws.cloudwatch.cloudwatch_helper import \
    CloudwatchHelper


def get_aws_example_config_file_path(file_name):
    import ray.autoscaler.aws
    return os.path.join(
        os.path.dirname(ray.autoscaler.aws.__file__), file_name)


def load_aws_example_config_file(file_name):
    config_file_path = get_aws_example_config_file_path(file_name)
    return yaml.safe_load(open(config_file_path).read())


def bootstrap_aws_config(config):
    config = prepare_config(config)
    validate_config(config)
    config["cluster_name"] = DEFAULT_CLUSTER_NAME
    return ray.autoscaler._private.aws.config.bootstrap_aws(config)


def bootstrap_aws_example_config_file(file_name):
    config = load_aws_example_config_file(file_name)
    return bootstrap_aws_config(config)


def get_cloudwatch_agent_config_file_path():
    return get_aws_example_config_file_path(
        "cloudwatch/example-cloudwatch-agent-config.json")


def get_cloudwatch_dashboard_config_file_path():
    return get_aws_example_config_file_path(
        "cloudwatch/example-cloudwatch-dashboard-config.json")


def get_cloudwatch_alarm_config_file_path():
    return get_aws_example_config_file_path(
        "cloudwatch/example-cloudwatch-alarm-config.json")


def load_cloudwatch_example_config_file():
    config = load_aws_example_config_file("example-cloudwatch.yaml")
    cw_cfg = config["provider"]["cloudwatch"]
    cw_cfg["agent"]["config"] = get_cloudwatch_agent_config_file_path()
    cw_cfg["dashboard"]["config"] = get_cloudwatch_dashboard_config_file_path()
    cw_cfg["alarm"]["config"] = get_cloudwatch_alarm_config_file_path()
    return config


def get_cloudwatch_helper(node_ids):
    config = load_cloudwatch_example_config_file()
    config["cluster_name"] = DEFAULT_CLUSTER_NAME
    return CloudwatchHelper(
        config["provider"],
        node_ids,
        config["cluster_name"],
    )


def get_ssm_param_name(cluster_name, section_name):
    ssm_config_param_name = "ray_cloudwatch_{}_config_{}".format(
        section_name, cluster_name)
    return ssm_config_param_name
