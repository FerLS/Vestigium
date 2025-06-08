using UnityEngine;
using UnityEngine.SceneManagement;

public class MainMenuManager : MonoBehaviour
{
    public static MainMenuManager _; // Singleton instance
    [SerializeField] private bool _debugMode;
    public enum MainMenuButtons { play, options, exit };
    public enum OptionsButtons { back };
    [SerializeField] GameObject _MainMenuContainer;
    [SerializeField] GameObject _OptionsMenuContainer;

    public void Awake()
    {
        // Singleton pattern implementation
        if (_ == null)
        {
            _ = this;
        }
        else if (_ != this)
        {
            Debug.LogError("There is more than one instance of MainMenuManager in the scene");
        }
    }

    private void Start()
    {
        // Initialize with main menu
        OpenMenu(_MainMenuContainer);
    }

    public void MainMenuButtonClicked(MainMenuButtons buttonClicked)
    {
        DebugMessage("Button clicked: " + buttonClicked.ToString());
        switch (buttonClicked)
        {
            case MainMenuButtons.play:
                PlayClicked();
                break;
            case MainMenuButtons.options:
                OptionsClicked();
                break;
            case MainMenuButtons.exit:
                Application.Quit();
                break;
            default:
                Debug.LogError("Unknown button clicked: " + buttonClicked.ToString());
                break;
        }
    }

    public void OptionsClicked()
    {
        OpenMenu(_OptionsMenuContainer);
    }

    public void ReturnToMainMenu()
    {
        OpenMenu(_MainMenuContainer);
    }

    public void OptionsButtonClicked(OptionsButtons buttonClicked)
    {
        switch (buttonClicked)
        {
            case OptionsButtons.back:
                ReturnToMainMenu();
                break;
        }
    }

    private void DebugMessage(string message)
    {
        // Output debug messages if debug mode is enabled
        if (_debugMode)
        {
            Debug.Log(message);
        }
    }

    public void PlayClicked()
    {
        SceneManager.Instance.ChangeToNextScene();
    }

    public void QuitGame()
    {
        // Handles quitting differently based on environment
#if UNITY_EDITOR
        UnityEditor.EditorApplication.ExitPlaymode();
#else
        Application.Quit();
#endif
    }

    public void OpenMenu(GameObject menuToOpen)
    {
        // Toggle visibility of menu containers
        _MainMenuContainer.SetActive(menuToOpen == _MainMenuContainer);
        _OptionsMenuContainer.SetActive(menuToOpen == _OptionsMenuContainer);
    }
}
