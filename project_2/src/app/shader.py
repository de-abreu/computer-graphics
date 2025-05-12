# pyright: reportCallIssue=false
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
    glUniform1f,
    glUniform1i,
)


class Shader:
    """
    A class to manage OpenGL shader programs, including compilation and linking.

    Attributes
    ----------
    id : int
        The OpenGL shader program ID.
    """

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
            program_id = glCreateProgram()
            if not program_id:
                raise RuntimeError("Failed to create shader program")
            self.id = program_id
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
        """
        Activate the shader program for rendering.

        Notes
        -----
        This must be called before issuing draw calls that use this shader.
        """
        glUseProgram(self.id)

    # utility functions
    def setBool(self, name: str, value: bool) -> None:
        """
        Set a boolean uniform in the shader.

        Parameters
        ----------
        name : str
            The name of the uniform variable in the shader.
        value : bool
            The boolean value to set.
        """
        glUniform1i(glGetUniformLocation(self.id, name), int(value))

    def setInt(self, name: str, value: int) -> None:
        """
        Set an integer uniform in the shader.

        Parameters
        ----------
        name : str
            The name of the uniform variable in the shader.
        value : int
            The integer value to set.
        """
        glUniform1i(glGetUniformLocation(self.id, name), value)

    def setFloat(self, name: str, value: float) -> None:
        """
        Set a float uniform in the shader.

        Parameters
        ----------
        name : str
            The name of the uniform variable in the shader.
        value : float
            The float value to set.
        """
        glUniform1f(glGetUniformLocation(self.id, name), value)

    def _checkCompileErrors(self, shader: int, type: str) -> None:
        """
        Check for shader or program compilation/linking errors.

        Parameters
        ----------
        shader : int
            The shader or program ID.
        type : str
            The type of shader ("VERTEX", "FRAGMENT", or "PROGRAM").

        Notes
        -----
        Prints compilation errors to the console if they occur.
        """
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
        """
        Compile a shader from source code.

        Parameters
        ----------
        shader_type : int
            The OpenGL shader type (e.g., `GL_VERTEX_SHADER`).
        shader_name : str
            A descriptive name for the shader (used in error messages).
        shader_definition : str
            The shader source code.

        Returns
        -------
        int
            The compiled shader ID.

        Notes
        -----
        Raises a RuntimeError if compilation fails.
        """
        shader = glCreateShader(shader_type)
        if not shader:
            raise RuntimeError("Shader compilation has failed")
        glShaderSource(shader, shader_definition)
        glCompileShader(shader)
        self._checkCompileErrors(shader, shader_name)
        return shader
