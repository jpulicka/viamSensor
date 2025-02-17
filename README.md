# Module sensor2 

This module will detect person in front of the camera. It uses a Vision service and a camera
## Model jpm:sensor2:helloPerson

This module will detect person in front of the camera. It uses a Vision service and a camera

### Configuration
The following attribute template can be used to configure this model:

```json
{
  "vision_service": "Name of the Vision Service",
  "actual_cam": "Name of the Camera"
}
```

#### Attributes

The following attributes are available for this model:

| Name             | Type   | Inclusion | Description                |
|------------------|--------|-----------|----------------------------|
| `vision_service` | string | Required  | Name of the Vision Service |
| `actual_cam`     | string | Required  | Name of the Camera         |

#### Example Configuration

```json
{
  "vision_service": "vision1",
  "actual_cam": "WebCamera"
}
```

### DoCommand

If your model implements DoCommand, provide an example payload of each command that is supported and the arguments that can be used. If your model does not implement DoCommand, remove this section.

#### Example DoCommand

```json
{
  "command_name": {
    "arg1": "foo",
    "arg2": 1
  }
}
```
