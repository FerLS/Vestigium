using System.Collections;
using System.Diagnostics;
using UnityEngine;
using UnityEngine.SceneManagement;
using static TransitionManager;
using UnitySceneManager = UnityEngine.SceneManagement.SceneManager;

public class SceneManager : MonoBehaviour
{
    // Singleton instance
    public static SceneManager Instance;

    private void Awake()
    {
        // Singleton pattern implementation
        if (Instance == null)
        {
            Instance = this;
            DontDestroyOnLoad(gameObject);
        }
        else
        {
            Destroy(gameObject);
        }
    }

    /// <summary>
    /// Changes to the next scene in build settings
    /// </summary>
    public void ChangeToNextScene(TransitionManager.TransitionType transitionType = TransitionManager.TransitionType.FadeOut)
    {
        int currentSceneIndex = UnitySceneManager.GetActiveScene().buildIndex;
        int nextSceneIndex = (currentSceneIndex + 1) % UnitySceneManager.sceneCountInBuildSettings;
        ChangeToScene(nextSceneIndex, transitionType);
    }

    /// <summary>
    /// Changes to a specific scene by index with transition effect
    /// </summary>
    public async void ChangeToScene(int sceneIndex, TransitionManager.TransitionType transitionType = TransitionManager.TransitionType.FadeOut)
    {
        await TransitionManager.Instance.PlayTransition(transitionType);
        UnitySceneManager.LoadScene(sceneIndex);
    }

    /// <summary>
    /// Reloads the current scene with transition effect
    /// </summary>
    public void ReloadCurrentScene(TransitionManager.TransitionType transitionType = TransitionManager.TransitionType.FadeOut)
    {
        int currentSceneIndex = UnitySceneManager.GetActiveScene().buildIndex;
        ChangeToScene(currentSceneIndex, transitionType);
    }
}
