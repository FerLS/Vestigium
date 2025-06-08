using UnityEngine;

public class Door : MonoBehaviour
{
    // Tracks if the door has been opened
    bool _opened = false;

    // Required key to open this door
    [SerializeField] private Pickable key;

    private void OnTriggerEnter(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            // Don't react if player is not grounded or door is already open
            if (!PlayerController.Instance.IsGrounded() || _opened) return;

            // Check if player is holding the required key
            if (!key.isHeld)
            {
                PlayerController.Instance.ShowInteractionText("You need a key to open this door.");
                return;
            }

            _opened = true;

            // Transition to the next scene with fade out effect
            SceneManager.Instance.ChangeToNextScene(TransitionManager.TransitionType.FadeOut);
        }
    }

    private void OnTriggerExit(Collider other)
    {
        if (other.CompareTag("Player"))
        {
            // Clear interaction text when player leaves the trigger area
            PlayerController.Instance.ShowInteractionText("");
        }
    }
}
