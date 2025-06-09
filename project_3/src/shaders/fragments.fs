#version 330 core
#define NUM_LIGHTS 3

// Define integer constants for locations.
#define LOCATION_INTERNAL 0
#define LOCATION_EXTERNAL 1
#define LOCATION_BOTH     2

// --- Light Source Struct ---
struct LightSource {
    vec3  position;
    vec3  color;
    float intensity;
    int   location; // Corresponds to LOCATION_INTERNAL, EXTERNAL, BOTH
};

// --- Uniforms ---
uniform LightSource lights[NUM_LIGHTS]; // Array of light source structs

// Global Lighting Parameters
uniform float ambient_intensity;
uniform vec3  ambient_color;

// Material Parameters
uniform float diffuse_intensity;
uniform float specular_intensity;
uniform float specular_exponent;

// Camera/View Parameters
uniform vec3 viewPos;

// Object-Specific Behavior Parameters
uniform bool is_emitter;       // Is this object a light source itself (and thus glows)?
uniform vec3 emission_color;   // If is_emitter, its glow color
uniform int  object_location;  // Location type of the current object being rendered

// Varying Inputs
varying vec2 out_textureCoords;
varying vec3 out_normal;
varying vec3 out_fragPos;

// Texture Sampler
uniform sampler2D samplerTexture;

void main() {
    vec4 textureColor = texture2D(samplerTexture, out_textureCoords);

    // 1. Handle Emissive Objects (Light source objects glow)
    if (is_emitter) {
        gl_FragColor = vec4(emission_color, textureColor.a);
        return; // No further lighting for purely emissive surfaces
    }

    // 2. Prepare common vectors
    vec3 norm = normalize(out_normal);
    vec3 viewDir = normalize(viewPos - out_fragPos);

    // 3. Ambient Lighting
    vec3 ambientReflection = ambient_intensity * ambient_color * textureColor.rgb;

    // Initialize accumulators
    vec3 totalDiffuse = vec3(0.0);
    vec3 totalSpecular = vec3(0.0);

    // 4. Loop Through Light Sources
    for (int i = 0; i < NUM_LIGHTS; ++i) {
        // Rule 2: Location-based light affection
        // Accessing struct members: lights[i].location
        if (lights[i].location == object_location ||
            lights[i].location == LOCATION_BOTH ||
            object_location == LOCATION_BOTH) {
            // Accessing struct members: lights[i].color, lights[i].intensity, lights[i].position
            vec3 currentLightEffectiveColor = lights[i].color * lights[i].intensity;

            // Diffuse
            vec3 lightDir = normalize(lights[i].position - out_fragPos);
            float diffFactor = max(dot(norm, lightDir), 0.0);
            vec3 diffuseComponent = diffuse_intensity * diffFactor * currentLightEffectiveColor;
            totalDiffuse += diffuseComponent;

            // Specular
            vec3 reflectDir = reflect(-lightDir, norm);
            float specFactor = pow(max(dot(viewDir, reflectDir), 0.0), specular_exponent);
            vec3 specularComponent = specular_intensity * specFactor * currentLightEffectiveColor;
            totalSpecular += specularComponent;
        }
    }

    // 5. Combine Lighting Components
    vec3 finalColor = ambientReflection + (totalDiffuse * textureColor.rgb) + totalSpecular;
    
    gl_FragColor = vec4(finalColor, textureColor.a);
}
