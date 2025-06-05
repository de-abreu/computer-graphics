#version 330 core
#define NUM_LIGHTS 3

// --- Global Lighting Parameters ---
uniform float u_ambientStrength;      // Coefficient for ambient reflection (Ka)
uniform vec3  u_globalAmbientColor;   // Color of the global ambient light (e.g., vec3(0.1, 0.1, 0.1) or higher)

// --- Material Parameters (Phong coefficients) ---
uniform float u_diffuseStrength;    // Coefficient for diffuse reflection (Kd)
uniform float u_specularStrength;   // Coefficient for specular reflection (Ks)
uniform float u_specularExponent;   // Shininess factor for specular highlights

// --- Light Source Parameters (Array for 3 lights) ---

uniform vec3 u_lightPositions[NUM_LIGHTS];   // Positions of the 3 light sources
uniform vec3 u_lightColors[NUM_LIGHTS];      // Colors of the 3 light sources
uniform float u_lightIntensities[NUM_LIGHTS]; // Intensities of the 3 light sources

// --- Camera/View Parameters ---
uniform vec3 u_viewPos;             // Position of the camera/observer

// --- Object-Specific Behavior Parameters ---
uniform bool u_isEmitter;                   // Is this object an emitter?
uniform vec3 u_emissionColor;               // If so, what is its emission color?
uniform bool u_affectedByColoredLights;     // Does this object react to colored lights?
uniform bool u_affectedByWhiteLight;        // Does this object react to the white light?
uniform int  u_whiteLightIndex;             // Index (0, 1, or 2) of the white light source

// --- Varying Inputs from Vertex Shader ---
varying vec2 out_textureCoords;     // Texture coordinates
varying vec3 out_normal;            // Normal vector (in world space)
varying vec3 out_fragPos;           // Fragment position (in world space)

// --- Texture Sampler ---
uniform sampler2D samplerTexture;

void main() {
    vec4 textureColor = texture2D(samplerTexture, out_textureCoords);

    // 1. Handle Emissive Objects
    if (u_isEmitter) {
        // Emissive objects might still use their texture to modulate emission, or just glow
        gl_FragColor = vec4(u_emissionColor * textureColor.rgb, textureColor.a);
        // Or, for a pure glow without texture influence on color:
        // gl_FragColor = vec4(u_emissionColor, textureColor.a);
        return; // No further lighting calculations for emitters
    }

    // 2. Prepare common vectors
    vec3 norm = normalize(out_normal);
    vec3 viewDir = normalize(u_viewPos - out_fragPos);

    // 3. Ambient Lighting
    // The ambient contribution is from a global ambient light source, reflected by the object's color
    vec3 ambientReflection = u_ambientStrength * u_globalAmbientColor * textureColor.rgb;

    // Initialize accumulators for diffuse and specular contributions from all relevant lights
    vec3 totalDiffuse = vec3(0.0);
    vec3 totalSpecular = vec3(0.0);

    // 4. Loop Through Light Sources
    for (int i = 0; i < NUM_LIGHTS; ++i) {
        bool isCurrentLightWhite = (i == u_whiteLightIndex);
        bool applyThisLight = false;

        if (isCurrentLightWhite && u_affectedByWhiteLight) {
            applyThisLight = true;
        } else if (!isCurrentLightWhite && u_affectedByColoredLights) {
            applyThisLight = true;
        }

        if (applyThisLight) {
            // Effective light color considering intensity
            vec3 currentLightEffectiveColor = u_lightColors[i] * u_lightIntensities[i];

            // Diffuse Calculation
            vec3 lightDir = normalize(u_lightPositions[i] - out_fragPos);
            float diffFactor = max(dot(norm, lightDir), 0.0);
            vec3 diffuseComponent = u_diffuseStrength * diffFactor * currentLightEffectiveColor;
            totalDiffuse += diffuseComponent;

            // Specular Calculation
            vec3 reflectDir = reflect(-lightDir, norm);
            float specFactor = pow(max(dot(viewDir, reflectDir), 0.0), u_specularExponent);
            vec3 specularComponent = u_specularStrength * specFactor * currentLightEffectiveColor;
            totalSpecular += specularComponent;
        }
    }

    // 5. Combine Lighting Components
    // Diffuse reflection is modulated by the object's texture color
    // Specular reflection is generally the color of the light itself (shiny highlights)
    vec3 finalColor = ambientReflection + (totalDiffuse * textureColor.rgb) + totalSpecular;
    
    // Gamma correction approximation (optional, but often good)
    // finalColor = pow(finalColor, vec3(1.0/2.2));


    gl_FragColor = vec4(finalColor, textureColor.a);
}
