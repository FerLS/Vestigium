using UnityEngine;
using System.Collections.Generic;

public class EyeLightController : MonoBehaviour
{
    [Header("Target Tracking")]
    [SerializeField] private float timeLookingAtTarget = 3f;
    [SerializeField] private float rotationSpeed = 5f;
    [SerializeField] private float idleOscillationAmplitude = 2f;
    [SerializeField] private float idleOscillationSpeed = 2f;

    [Header("Light Component (optional)")]
    [SerializeField] private Light lightComponent;

    private List<Transform> targets = new List<Transform>();
    private Transform currentTarget;
    private float targetTimer;
    private bool firstTargetSet;

    [Header("Audio")]
    [SerializeField] private AudioClip continuous;
    [SerializeField] private AudioClip change_target;

    private void Awake()
    {
        // Get light component if not assigned
        if (lightComponent == null)
            lightComponent = GetComponent<Light>();
    }

    private void Start()
    {
        AudioManager.Instance.PlayLoopSFX3D("tv", continuous, transform);
        FindAllTargets();
        SelectInitialTarget();
    }

    private void Update()
    {
        if (currentTarget == null) return;

        targetTimer += Time.deltaTime;
        RotateTowardsTarget();
        ApplyIdleOscillation();

        // Change target after set time
        if (targetTimer >= timeLookingAtTarget)
        {
            PickNewTarget();
        }
    }

    private void FindAllTargets()
    {
        // Find all obstacles and add to targets list
        GameObject[] obstacles = GameObject.FindGameObjectsWithTag("Obstacle");
        foreach (GameObject obj in obstacles)
        {
            targets.Add(obj.transform);
        }

        if (targets.Count == 0)
        {
            Debug.LogWarning("No objects found with 'Obstacle' tag.");
            enabled = false;
        }
    }

    private void SelectInitialTarget()
    {
        // Try to find specific initial target first
        GameObject obstacle1 = GameObject.Find("Obstacle1");
        if (obstacle1 != null)
        {
            currentTarget = obstacle1.transform;
            firstTargetSet = true;
        }
        else if (targets.Count > 0)
        {
            PickNewTarget();
        }
    }

    private void RotateTowardsTarget()
    {
        // Smoothly rotate toward current target
        Vector3 direction = currentTarget.position - transform.position;
        Quaternion targetRotation = Quaternion.LookRotation(direction);
        transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.deltaTime * rotationSpeed);
    }

    private void ApplyIdleOscillation()
    {
        // Add small random movement while tracking target
        if (targetTimer < timeLookingAtTarget)
        {
            float x = Mathf.Sin(Time.time * idleOscillationSpeed) * idleOscillationAmplitude;
            float y = Mathf.Cos(Time.time * idleOscillationSpeed * 0.8f) * idleOscillationAmplitude;
            transform.rotation *= Quaternion.Euler(x, y, 0f);
        }
    }

    private void PickNewTarget()
    {
        targetTimer = 0f;

        if (firstTargetSet)
        {
            firstTargetSet = false;
            return;
        }

        if (targets.Count < 2) return;

        // Select random target different from current
        Transform newTarget = currentTarget;
        while (newTarget == currentTarget)
        {
            newTarget = targets[Random.Range(0, targets.Count)];
        }
        AudioManager.Instance.PlaySFX(change_target);

        currentTarget = newTarget;
    }
}