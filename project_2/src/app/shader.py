from OpenGL.GL import (
    GL_COMPILE_STATUS,
    GL_LINK_STATUS,
    GL_VERTEX_SHADER,
    GL_FRAGMENT_SHADER,
    glCreateShader,
    glCompileShader,
    glGetProgramInfoLog,
    glGetProgramiv,
    glGetShaderInfoLog,
    glGetShaderiv,
    glGetUniformLocation,
    glShaderSource,
    glCreateProgram,
    glAttachShader,
    glLinkProgram,
    glDeleteShader,
    glUseProgram,
)
from OpenGL.GL.VERSION.GL_2_0 import glUniform1f, glUniform1i


class Shader:
    id: int

    def __init__(self, vertexPath: str, fragmentPath: str):
        try:
            # Compile shaders
            with (
                open(vertexPath) as vShaderFile,
                open(fragmentPath) as fShaderFile,
            ):
                vertex = self._compile_shader(
                    GL_VERTEX_SHADER, "VERTEX", vShaderFile.read()
                )
                fragment = self._compile_shader(
                    GL_FRAGMENT_SHADER, "FRAGMENT", fShaderFile.read()
                )

            # Create shader program
            self.id = glCreateProgram()
            glAttachShader(self.id, vertex)
            glAttachShader(self.id, fragment)
            glLinkProgram(self.id)
            self._checkCompileErrors(self.id, "PROGRAM")
            # delete the shaders as they're linked into our program now and no longer necessary
            glDeleteShader(vertex)
            glDeleteShader(fragment)

        except IOError:
            print("ERROR::SHADER::FILE_NOT_SUCCESFULLY_READ")

    # get program
    # ------------------------------------------------------------------------
    def getProgram(self):
        return self.id

    # activate the shader
    # ------------------------------------------------------------------------
    def use(self) -> None:
        glUseProgram(self.id)

    # utility functions
    def setBool(self, name: str, value: bool) -> None:
        glUniform1i(glGetUniformLocation(self.id, name), int(value))

    def setInt(self, name: str, value: int) -> None:
        glUniform1i(glGetUniformLocation(self.id, name), value)

    def setFloat(self, name: str, value: float) -> None:
        glUniform1f(glGetUniformLocation(self.id, name), value)

    def _checkCompileErrors(self, shader: int, type: str) -> None:
        if type != "PROGRAM":
            if glGetShaderiv(shader, GL_COMPILE_STATUS):
                return
            infoLog = glGetShaderInfoLog(shader)
        else:
            if glGetProgramiv(shader, GL_LINK_STATUS):
                return
            infoLog = glGetProgramInfoLog(shader)
        print(
            "ERROR::SHADER_COMPILATION_ERROR of type: "
            + type
            + "\n"
            + infoLog.decode()
            + "\n -- --------------------------------------------------- -- "
        )

    def _compile_shader(
        self, shader_type: int, shader_name: str, shader_definition: str
    ) -> int:
        shader = glCreateShader(shader_type)
        glShaderSource(shader, shader_definition)
        glCompileShader(shader)
        self._checkCompileErrors(shader, shader_name)
        return shader
