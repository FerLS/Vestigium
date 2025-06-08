using UnityEngine;

[RequireComponent(typeof(Light))]
public class LightCollisionDetection : MonoBehaviour
{
    [SerializeField] private Light lightComponent;

    private void Awake()
    {
        // Get the Light component if not assigned
        if (lightComponent == null)
            lightComponent = GetComponent<Light>();

        // Register this detector with the group manager
        LightCollisionDetectorGroup.Register(this);
    }

    private void OnDestroy()
    {
        // Unregister when destroyed to prevent memory leaks
        LightCollisionDetectorGroup.Unregister(this);
    }

    public bool IsInLightCone(Transform target)
    {
        // Return false if light is disabled or inactive
        if (!lightComponent.enabled || !lightComponent.gameObject.activeInHierarchy)
            return false;

        Vector3 toTarget = target.position - lightComponent.transform.position;
        float distance = toTarget.magnitude;

        // Check if target is within light range
        if (distance > lightComponent.range)
            return false;

        // Check if target is within the spotlight angle
        float angle = Vector3.Angle(lightComponent.transform.forward, toTarget);
        if (angle > lightComponent.spotAngle / 2f)
            return false;

        // Check if there's an obstacle between the light and target
        if (Physics.Raycast(lightComponent.transform.position, toTarget.normalized, out RaycastHit hit, distance))
        {
            return hit.transform == target;
        }

        return false;
    }

    private void OnDrawGizmosSelected()
    {
        // Visualize light direction in editor
        if (lightComponent == null) return;

        Gizmos.color = Color.yellow;
        Gizmos.DrawRay(lightComponent.transform.position, lightComponent.transform.forward * lightComponent.range);
    }
}
