using UnityEngine;

[RequireComponent(typeof(Light))]
public class LightFlicker : MonoBehaviour
{
    [Header("Flicker Settings")]
    [SerializeField] private float minIntensity = 0.05f;  // Minimum light intensity
    [SerializeField] private float maxIntensity = 1.2f;   // Maximum light intensity
    [SerializeField] private float flickerSpeedMin = 0.05f;  // Minimum time between flickers
    [SerializeField] private float flickerSpeedMax = 0.3f;   // Maximum time between flickers

    [Header("Light Component")]
    [SerializeField] private Light lightComponent;

    private float targetIntensity;   // Intensity value we're moving toward
    private float currentIntensity;  // Current intensity value
    private float nextFlickerTime;   // Time when next flicker should occur

    private void Awake()
    {
        // Get light component if not assigned
        if (lightComponent == null)
            lightComponent = GetComponent<Light>();
    }

    private void Start()
    {
        currentIntensity = lightComponent.intensity;
        ScheduleNextFlicker();
    }

    private void Update()
    {
        // Time to change intensity target
        if (Time.time >= nextFlickerTime)
        {
            // 10% chance for min intensity, otherwise random between min and max
            targetIntensity = Random.value < 0.1f
                ? minIntensity
                : Random.Range(minIntensity, maxIntensity);

            ScheduleNextFlicker();
        }

        // Smoothly transition to target intensity
        currentIntensity = Mathf.Lerp(currentIntensity, targetIntensity, Time.deltaTime * 20f);
        lightComponent.intensity = currentIntensity;
    }

    private void ScheduleNextFlicker()
    {
        // Set next flicker time based on defined speed range
        nextFlickerTime = Time.time + Random.Range(flickerSpeedMin, flickerSpeedMax);
    }
}