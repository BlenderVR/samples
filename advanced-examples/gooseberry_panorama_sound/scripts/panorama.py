import bge
from bge import logic, render

LEFT_EYE = bge.render.LEFT_EYE
RIGHT_EYE = bge.render.RIGHT_EYE


def init():
    # 1. create a custom shader for the sphere
    # 2. update the shader uniform during pre_draw

    scene = logic.getCurrentScene()
    logic.shader_object = ShaderObject(
            scene.objects.get('Icosphere'),
            scene.objects.get('Camera'),
            )

    scene.pre_draw.append(pre_draw)


def pre_draw():
    logic.shader_object.update()


class ShaderObject():
    _VertexShader = """
varying vec4 coord_vec;

void main() {
    coord_vec = gl_Vertex;
    gl_Position = gl_ModelViewProjectionMatrix * coord_vec;
}
"""

    _FragmentShader = """
uniform sampler2D panorama;
uniform float image_offset;
uniform vec3 camera_position;

varying vec4 coord_vec;

#define M_PI_F  3.141592653589793
#define M_2PI_F 6.283185307179586

vec2 direction_to_equirectangular(vec3 dir)
{
    float u = -atan(dir.x, dir.y)/(M_2PI_F) + 0.5;
    float v = atan(dir.z, sqrt(dir.x * dir.x + dir.y * dir.y))/M_PI_F + 0.5;

    return vec2(u, v);
}

void main() {
    vec3 world_position = coord_vec.xyz;
    vec3 dir = world_position - camera_position;

    dir = normalize(dir);
    vec2 coords = direction_to_equirectangular(dir);

    coords.y = coords.y * 0.5 + image_offset;

    gl_FragColor = texture2D(panorama, coords);
}
"""
    def __init__(self, shader_object, camera):
        self._shader_object = shader_object
        self._camera_position = camera.worldPosition
        self._image_offset = 0.5
        self.update()


    def _shader(self):
        for mesh in self._shader_object.meshes:
            for material in mesh.materials:
                shader = material.getShader()

            if shader != None:
                if not shader.isValid():
                    shader.setSource(self._VertexShader, self._FragmentShader, True)

                shader.setSampler('panorama', 0)
                shader.setUniform1f('image_offset', self._image_offset)
                shader.setUniformfv('camera_position', self._camera_position)


    def update(self):
        if render.getStereoEye() == LEFT_EYE:
            self._image_offset = 0.0
        else:
            self._image_offset = 0.5

        self._shader()
