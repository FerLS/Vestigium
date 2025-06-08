using System;
using UnityEngine;

public class Pickable : Interactable
{
    private Rigidbody rb;
    private Collider col;
    public bool isHeld { get; private set; }

    // Reference to player's holding position
    private Transform playerHoldPoint => PlayerController.Instance.HoldPoint;

    protected override void Start()
    {
        isHeld = false;
        rb = GetComponent<Rigidbody>();
        col = GetComponent<Collider>();
        interactionType = InteractionType.PickUp;
        base.Start();
    }

    public override void OnStartInteraction()
    {
        if (!isHeld)
        {
            Debug.Log("OnStartInteraction: Object not currently held.");
            PickUp(playerHoldPoint);
            isHeld = true;
        }
    }

    public override void OnStopInteraction()
    {
        if (isHeld)
        {
            Drop();
            isHeld = false;
        }
    }

    // Attaches object to the hold point and disables physics
    private void PickUp(Transform holdPoint)
    {
        Debug.Log("Picking up object.");

        transform.SetParent(holdPoint);
        transform.localPosition = Vector3.zero;
        transform.localRotation = Quaternion.identity;

        if (rb != null) rb.isKinematic = true;
        if (col != null) col.enabled = false;
    }

    // Releases object and re-enables physics
    private void Drop()
    {
        transform.SetParent(null);

        if (rb != null) rb.isKinematic = false;
        if (col != null) col.enabled = true;
    }
}
