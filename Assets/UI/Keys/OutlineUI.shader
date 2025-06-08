Shader "UI/OutlineUI"
{
    Properties
    {
        _MainTex ("Texture", 2D) = "white" {}
        _OutlineColor ("Outline Color", Color) = (1,1,1,1)
        _OutlineThickness ("Outline Thickness", Range(0.0, 10.0)) = 1.0
        _GlowIntensity ("Glow Intensity (HDR)", Range(0, 10)) = 1.0
    }

    SubShader
    {
        Tags { "RenderType"="Transparent" "Queue"="Transparent" }
        LOD 100

        Pass
        {
            Name "UIOutlinePass"
            Tags { "LightMode"="UniversalForward" }

            Blend SrcAlpha OneMinusSrcAlpha
            Cull Off
            ZWrite Off

            HLSLPROGRAM
            #pragma vertex vert
            #pragma fragment frag
            #include "Packages/com.unity.render-pipelines.universal/ShaderLibrary/Core.hlsl"

            struct Attributes
            {
                float4 positionOS : POSITION;
                float2 uv : TEXCOORD0;
            };

            struct Varyings
            {
                float4 positionHCS : SV_POSITION;
                float2 uv : TEXCOORD0;
            };

            sampler2D _MainTex;
            float4 _MainTex_ST;
            float4 _OutlineColor;
            float _OutlineThickness;
            float _GlowIntensity;

            Varyings vert(Attributes v)
            {
                Varyings o;
                o.positionHCS = TransformObjectToHClip(v.positionOS);
                o.uv = TRANSFORM_TEX(v.uv, _MainTex);
                return o;
            }

            float4 frag(Varyings i) : SV_Target
            {
                float2 uv = i.uv;

                float4 baseColor = tex2D(_MainTex, uv);
                float alpha = baseColor.a;

                // Sobremuestreo del alpha alrededor del píxel para crear outline
                float outline = 0.0;
                float2 pixelSize = float2(_OutlineThickness / _ScreenParams.x, _OutlineThickness / _ScreenParams.y);

                for (int x = -1; x <= 1; x++)
                {
                    for (int y = -1; y <= 1; y++)
                    {
                        float2 offset = float2(x, y) * pixelSize;
                        float4 sample = tex2D(_MainTex, uv + offset);
                        outline += step(0.1, sample.a); // si hay algo visible, cuenta para el contorno
                    }
                }

                outline = saturate(outline / 9.0); // normalizamos

                // Si el píxel es transparente pero alrededor hay opacos, renderizamos contorno
                if (alpha < 0.1 && outline > 0.0)
                {
                    return _OutlineColor * _GlowIntensity;
                }

                return baseColor;
            }
            ENDHLSL
        }
    }

    FallBack "Hidden/Universal Render Pipeline/FallbackError"
}
