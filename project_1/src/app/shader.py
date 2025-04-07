from OpenGL.GL import (
    GL_COMPILE_STATUS,
    GL_FRAGMENT_SHADER,
    GL_LINK_STATUS,
    GL_VERTEX_SHADER,
    glAttachShader,
    glCompileShader,
    glCreateProgram,
    glCreateShader,
    glGetProgramiv,
    glGetShaderiv,
    glLinkProgram,
    glShaderSource,
    glUseProgram,
)


def compile_shader(source: str, shader_type: int) -> int:
    """
    Compiles a shader from the given source code.

    This function creates a shader object of the specified type, sets its source code,
    compiles it, and checks for compilation errors.

    Args:
        source (str): The source code of the shader as a string.
        shader_type (int): The type of shader to create. Must be either `GL_VERTEX_SHADER` or `GL_FRAGMENT_SHADER`.

    Returns:
        int: The handle of the compiled shader object.

    Raises:
        RuntimeError: If the shader compilation fails.

    Note:
        The shader source code is expected to be in GLSL (OpenGL Shading Language) syntax.
        The compiled shader object must be attached to a program object using `glAttachShader` before it can be used.
    """
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        raise RuntimeError("Shader compilation error")
    return shader


def create_shader_program(vertex_source: str, fragment_source: str) -> int:
    """
    Creates and links a shader program from vertex and fragment shaders.

    This function compiles the vertex and fragment shaders, creates a program object,
    attaches the shaders to it, links the program, and checks for linking errors.
    The program is then installed as part of the current rendering state.

    Args:
        vertex_source (str): The source code of the vertex shader as a string.
        fragment_source (str): The source code of the fragment shader as a string.

    Returns:
        int: The handle of the linked shader program object.

    Raises:
        RuntimeError: If the shader program linking fails.

    Note:
        The shader program is automatically installed as part of the current rendering state.
        You can switch to a different program using `glUseProgram`.
        It is the caller's responsibility to delete the shader objects after linking the program.
        You can do this by calling `glDeleteShader` on the shader handles returned by `compile_shader`.
    """
    program = glCreateProgram()
    vertex = compile_shader(vertex_source, GL_VERTEX_SHADER)
    fragment = compile_shader(fragment_source, GL_FRAGMENT_SHADER)
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)
    if not glGetProgramiv(program, GL_LINK_STATUS):
        raise RuntimeError("Shader linking error")

    glUseProgram(program)
    return program
