using UnityEngine;
using UnityEngine.SceneManagement;

public class SceneTrigger : MonoBehaviour
{
    // Called when another collider enters this trigger collider
    private void OnTriggerEnter(Collider other)
    {
        // Check if the entering object is tagged as "Player"
        if (other.CompareTag("Player"))
        {
            // Transition to the next scene using a fade out effect
            SceneManager.Instance.ChangeToNextScene(TransitionManager.TransitionType.FadeOut);
        }
    }
}
