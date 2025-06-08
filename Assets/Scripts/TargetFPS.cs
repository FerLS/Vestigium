using UnityEngine;

public class TargetFPS : MonoBehaviour
{
    void Awake()
    {
        Application.targetFrameRate = 60; // Set the target frame rate to 60 FPS
    }
}
