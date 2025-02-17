import asyncio
import random
from typing import Any, ClassVar, Final, List, Mapping, Optional, Sequence, Dict, cast

from typing_extensions import Self
from viam.components.sensor import *
from viam.module.module import Module
from viam.proto.app.robot import ComponentConfig
from viam.proto.common import Geometry, ResourceName
from viam.resource.base import ResourceBase
from viam.resource.easy_resource import EasyResource
from viam.resource.types import Model, ModelFamily
from viam.utils import SensorReading, ValueTypes
from viam.components.camera import Camera
from viam.services.vision import VisionClient, Vision


class Helloperson(Sensor, EasyResource):
    MODEL: ClassVar[Model] = Model(ModelFamily("jpm", "sensor2"), "helloPerson")
    #camera: Camera
    #detector: VisionClient
    def __init__(self, name: str):
        super().__init__(name)
        self.actual_cam = None
        self.vision_service = None

    @classmethod
    def new(
        cls, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ) -> Self:
        return super().new(config, dependencies)

    @classmethod
    def validate_config(cls, config: ComponentConfig) -> Sequence[str]:
        actual_cam = config.attributes.fields["actual_cam"].string_value
        vision_service = config.attributes.fields["vision_service"].string_value
        if actual_cam == "":
            raise Exception("actual_cam attribute is required")
        if vision_service == "":
            raise Exception("vision_service attribute is required")
        return [actual_cam, vision_service]

        #return ["rdk:component:camera:myCam", "rdk:service:vision:visionService"]
        #return ["myCam", "visionService"]

    def reconfigure(
        self, config: ComponentConfig, dependencies: Mapping[ResourceName, ResourceBase]
    ):
        actual_cam_name = config.attributes.fields["actual_cam"].string_value
        vision_service_name = config.attributes.fields["vision_service"].string_value
        actual_cam = dependencies[Camera.get_resource_name(actual_cam_name)]
        vision_service = dependencies[Vision.get_resource_name(vision_service_name)]
        self.actual_cam = cast(Camera, actual_cam)
        self.vision_service = cast(Vision, vision_service)
        return super().reconfigure(config, dependencies)

    async def get_readings(
        self,
        *,
        extra: Optional[Mapping[str, Any]] = None,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, SensorReading]:

        number = random.random()
        detections = await self.vision_service.get_detections_from_camera(self.actual_cam.name)

        person_detected = "No"
        for detection in detections:
            if detection.class_name.lower() == "person":
                person_detected = "Yes"
                break

        return {
            "random_number": number,
            "Statement": "woohooo",
            "person_detected": person_detected
        }

    async def do_command(
        self,
        command: Mapping[str, ValueTypes],
        *,
        timeout: Optional[float] = None,
        **kwargs
    ) -> Mapping[str, ValueTypes]:
        raise NotImplementedError()

    async def get_geometries(
        self, *, extra: Optional[Dict[str, Any]] = None, timeout: Optional[float] = None
    ) -> List[Geometry]:
        raise NotImplementedError()


if __name__ == "__main__":
    asyncio.run(Module.run_from_registry())

