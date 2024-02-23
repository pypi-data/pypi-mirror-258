from kubernetes_utils.custom_object import CustomObject
from typing import TypeVar

T = TypeVar('T')


class RebootCustomObject(CustomObject[T]):
    """
    This Python class wraps a k8s custom object with the appropriate
    configuration for Reboot objects.
    """

    group: str = 'reboot.dev'
    version: str = 'v1'
