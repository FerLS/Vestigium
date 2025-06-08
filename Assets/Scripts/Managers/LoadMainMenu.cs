using UnityEngine;

public class LoadMainMenu : MonoBehaviour
{
    private void OnEnable()
    {
        // Load main menu scene when this GameObject is enabled
        SceneManager.Instance.ChangeToScene(0);
    }
}