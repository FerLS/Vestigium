using System.Threading.Tasks;
using UnityEngine;
using DG.Tweening;
using System;
using UnityEngine.UIElements;
using TMPro;
using System.Collections.Generic;

public class PlayerController : MonoBehaviour
{
    public static PlayerController Instance { get; private set; }
    InputSystem_Actions inputActions;

    [Header("Components")]
    [SerializeField] private Rigidbody rb;
    [SerializeField] private Animator anim;
    [SerializeField] private TextMeshProUGUI interactionText;

    [Header("Movement")]
    [SerializeField] private float acceleration = 1f;
    [SerializeField] private float maxSpeed = 10f;
    [SerializeField] private float runMultiplier = 1.5f;
    [SerializeField] private float jumpForce = 5f;
    [SerializeField] private float jumpDelay = 0.1f;

    bool _isDead = false;
    bool _isRunning = false;
    bool _isMoving = false;
    bool _isJumping = false;
    bool _onGround = false;
    bool _onTransition = false;

    [Header("Pull Push")]
    int _grabbing = 0; // 0 Not Grabbing, 1 Grabbing, 2 Pushing, 3 Pulling
    [SerializeField] float pushPullMultiplier = 0.5f;
    Vector3 grabDirection; // Fixed direction while grabbing

    [Header("Hang")]
    [SerializeField] private Collider hangCollider;

    [Header("Pick Up")]
    [SerializeField] private Transform holdPoint;  // Empty object where items will be held
    public Transform HoldPoint => holdPoint;

    private InteractionTrigger nearbyTrigger; // Reference to active trigger

    [Header("Audio")]
    [SerializeField] private AudioClip deathSound;

    private void Awake()
    {
        Instance = this;
        inputActions = new InputSystem_Actions();
    }

    private void OnEnable()
    {
        inputActions.Enable();

        inputActions.Player.Jump.performed += _ => Jump();
        inputActions.Player.Move.performed += _ => { _isMoving = true; anim.SetBool("isMoving", _isMoving); };
        inputActions.Player.Move.canceled += _ => { _isMoving = false; anim.SetBool("isMoving", _isMoving); if (_grabbing != 0) anim.SetInteger("isGrabbing", 1); };
        inputActions.Player.Run.performed += _ => { _isRunning = true; anim.SetBool("isRunning", _isRunning); };
        inputActions.Player.Run.canceled += _ => { _isRunning = false; anim.SetBool("isRunning", _isRunning); };

        inputActions.Player.BackFlip.performed += _ => anim.CrossFade("EsaCosa", 0.25f);
    }

    void Update()
    {
        _onGround = IsGrounded();
        anim.SetBool("onFloor", _onGround);

        // Check if player collides with harmful objects
        if (!_isDead && LightCollisionDetectorGroup.CollidesWithAny(transform))
        {
            KillPlayer();
        }
    }

    void FixedUpdate()
    {
        if (inputActions.Player.Move.IsPressed())
        {
            Vector2 moveInput = inputActions.Player.Move.ReadValue<Vector2>();
            Move(moveInput);
        }
    }

    void Move(Vector2 direction)
    {
        if (_onTransition) return; // Prevent movement during transitions

        Vector3 moveDirection = new Vector3(direction.x, 0, direction.y).normalized;
        float vel = _grabbing != 0 ? pushPullMultiplier : _isRunning ? runMultiplier : 1f;
        Quaternion targetRotation = transform.rotation;

        if (_grabbing != 0)
        {
            // ONLY movement in the grabDirection (forward or backward)
            float forwardAmount = Vector3.Dot(moveDirection, grabDirection.normalized);
            Vector3 projectedMove = grabDirection.normalized * forwardAmount; // Only forward/backward

            _grabbing = (forwardAmount > 0f) ? 2 : 3; // 2 = Push, 3 = Pull
            anim.SetInteger("isGrabbing", _grabbing);

            rb.AddForce(projectedMove.normalized * acceleration * vel, ForceMode.Acceleration);
            targetRotation = Quaternion.LookRotation(grabDirection); // Keep facing grab direction
        }
        else
        {
            // Normal movement
            targetRotation = Quaternion.LookRotation(moveDirection);
            rb.AddForce(moveDirection * acceleration * vel, ForceMode.Acceleration);
        }

        transform.rotation = Quaternion.Slerp(transform.rotation, targetRotation, Time.fixedDeltaTime * 10f);

        // Limit maximum speed
        if (rb.linearVelocity.magnitude >= maxSpeed)
        {
            rb.linearVelocity = new Vector3(
                rb.linearVelocity.normalized.x * maxSpeed * vel,
                rb.linearVelocity.y,
                rb.linearVelocity.normalized.z * maxSpeed * vel
            );
        }
    }

    async void Jump()
    {
        if (!IsGrounded() || _grabbing != 0 || _isJumping) return;

        anim.CrossFade(_isMoving ? "RunJump" : "Jump", 0.25f);

        if (!_isMoving)
        {
            _isJumping = true;
            anim.SetBool("isJumping", _isJumping);
            await Task.Delay((int)(jumpDelay * 600));
        }

        rb.AddForce(Vector3.up * jumpForce, ForceMode.Impulse);
        await Task.Delay(500);
        _isJumping = false;
        anim.SetBool("isJumping", _isJumping);
    }

    public bool IsGrounded()
    {
        return Physics.Raycast(transform.position, Vector3.down, 1.1f);
    }

    // Called from animation events to play footstep sounds
    public void OnFootstep()
    {
        if (!_onGround || !_isMoving || _onTransition)
            return;

        string surface = "Default";
        RaycastHit hit;
        if (Physics.Raycast(transform.position + Vector3.up * 0.1f, Vector3.down, out hit, 2f))
        {
            if (hit.collider.sharedMaterial != null)
                surface = hit.collider.sharedMaterial.name;
        }

        AudioClip sound = SurfaceToSound.Instance?.GetSurfaceSound(surface);
        AudioManager.Instance.PlaySFX(sound, 0.5f);
    }

    // Handles starting different interaction types
    public async Task OnStartInteraction(Interactable.InteractionType interactionType, Transform target = null)
    {
        ShowInteractionText("");
        switch (interactionType)
        {
            case Interactable.InteractionType.PushPull:
                _grabbing = 1;
                _onTransition = true;
                _ = Task.Run(async () =>
                {
                    await Task.Delay(1000);
                    _onTransition = false;
                });

                if (target != null)
                {
                    Vector3 toObject = (target.position - transform.position);
                    toObject.y = 0;
                    grabDirection = toObject.normalized;

                    await transform.DORotateQuaternion(Quaternion.LookRotation(grabDirection), 0.25f).AsyncWaitForCompletion();
                    rb.linearVelocity = Vector3.zero; // Stop movement when grabbing
                    target.SetParent(transform); // Make object follow player
                }

                anim.SetInteger("isGrabbing", _grabbing);
                break;

            case Interactable.InteractionType.PickUp:
                Debug.Log("Pick up interaction started.");
                break;

            case Interactable.InteractionType.Closable:
                Debug.Log("Closable interaction started.");
                break;

            case Interactable.InteractionType.Switchable:
                Debug.Log("Switchable interaction started.");
                break;
        }
    }

    // Handles ending different interaction types
    public void OnStopInteraction(Interactable.InteractionType interactionType)
    {
        switch (interactionType)
        {
            case Interactable.InteractionType.PushPull:
                _grabbing = 0;
                grabDirection = Vector3.zero;
                anim.SetInteger("isGrabbing", _grabbing);
                break;

            case Interactable.InteractionType.PickUp:
                // Optional release logic
                break;
        }
    }

    async void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("HangPoint"))
        {
            // Check if the other object collided with the hang collider
            if (other.bounds.Intersects(hangCollider.bounds))
            {
                _onTransition = true;
                rb.isKinematic = true; // Disable physics when hanging
                anim.CrossFade("Hang", 0.1f); // Play hanging animation

                Vector3 targetPosition = transform.position + transform.forward * 0.6f; // Adjust position
                targetPosition = new Vector3(targetPosition.x, other.transform.position.y + 0.5f, targetPosition.z); // Adjust height

                // Get the contact point on the collider
                Vector3 contactPoint = other.ClosestPoint(transform.position);
                // Calculate direction from player to that point
                Vector3 directionToContactPoint = contactPoint - transform.position;
                // Keep rotation on horizontal plane
                directionToContactPoint.y = 0;

                transform.DORotateQuaternion(Quaternion.LookRotation(directionToContactPoint.normalized), 0.7f);
                await transform.DOMove(targetPosition, 1.2f).SetDelay(0.5f).AsyncWaitForCompletion();

                rb.isKinematic = false; // Re-enable physics
                _onTransition = false; // Allow movement again
            }
        }

        var trigger = other.GetComponent<InteractionTrigger>();
        if (trigger != null)
        {
            nearbyTrigger = trigger;
        }
    }

    private void OnTriggerExit(Collider other)
    {
        var trigger = other.GetComponent<InteractionTrigger>();
        if (trigger != null && trigger == nearbyTrigger)
        {
            nearbyTrigger = null;
        }
    }

    public void ShowInteractionText(string text)
    {
        interactionText.text = text;
    }

    public async void KillPlayer()
    {
        if (_isDead) return;
        _isDead = true;

        Debug.Log("Player is dead");
        anim.CrossFade("Diying", 0.1f);
        _onTransition = true;
        inputActions.Disable();
        AudioManager.Instance.PlaySFX(deathSound);

        Destroy(gameObject, 3f);
        await Task.Delay(2000);

        SceneManager.Instance.ReloadCurrentScene();
    }

    public void DisableControls()
    {
        inputActions.Disable();
        _onTransition = true;
    }

    public void EnableControls()
    {
        inputActions.Enable();
        _onTransition = false;
    }

    void OnDestroy()
    {
        inputActions.Disable();
    }
}
