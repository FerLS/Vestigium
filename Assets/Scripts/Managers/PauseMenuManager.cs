using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.InputSystem;

public class PauseMenuManager : MonoBehaviour
{
    // Singleton instance
    public static PauseMenuManager _;
    [SerializeField] private bool _debugMode;
    public enum PauseMenuButtons { resume, restart, options, quitToMain };
    public enum OptionsButtons { back };
    [SerializeField] private GameObject _PauseMenuContainer;
    [SerializeField] private GameObject _OptionsMenuContainer;
    InputSystem_Actions _inputActions;
    private bool _isPaused = false;

    private void Awake()
    {
        // Singleton pattern implementation
        if (_ == null) _ = this;
        else if (_ != this)
        {
            Debug.LogError("There is more than one instance of PauseMenuManager in the scene");
        }

        // Initialize input system
        _inputActions = new InputSystem_Actions();
        _inputActions.Enable();
        _inputActions.UI.Pause.performed += OnPausePressed;
    }

    private void Start()
    {
        _PauseMenuContainer.SetActive(false);
    }

    private void OnPausePressed(InputAction.CallbackContext context)
    {
        if (context.performed)
        {
            TogglePause();
        }
    }

    public void TogglePause()
    {
        if (_isPaused) Resume();
        else Pause();
    }

    private void Pause()
    {
        Time.timeScale = 0;
        _PauseMenuContainer.SetActive(true);
        _isPaused = true;
        DebugMessage("Game paused.");
    }

    public void Resume()
    {
        Time.timeScale = 1;
        _PauseMenuContainer.SetActive(false);
        _isPaused = false;
        DebugMessage("Game resumed.");
    }

    public void PauseMenuButtonClicked(PauseMenuButtons buttonClicked)
    {
        DebugMessage("Pause menu button clicked: " + buttonClicked.ToString());

        switch (buttonClicked)
        {
            case PauseMenuButtons.resume:
                Resume();
                break;
            case PauseMenuButtons.restart:
                Time.timeScale = 1;
                SceneManager.Instance.ReloadCurrentScene();
                break;
            case PauseMenuButtons.options:
                OptionsClicked();
                break;
            case PauseMenuButtons.quitToMain:
                Time.timeScale = 1;
                SceneManager.Instance.ChangeToScene(0); // Load main menu scene
                break;
        }
    }

    public void OptionsClicked()
    {
        OpenMenu(_OptionsMenuContainer);
    }

    public void ReturnToPauseMenu()
    {
        OpenMenu(_PauseMenuContainer);
    }

    public void OptionsButtonClicked(OptionsButtons buttonClicked)
    {
        switch (buttonClicked)
        {
            case OptionsButtons.back:
                ReturnToPauseMenu();
                break;
        }
    }

    private void DebugMessage(string message)
    {
        if (_debugMode)
        {
            Debug.Log(message);
        }
    }

    // Shows the specified menu and hides others
    public void OpenMenu(GameObject menuToOpen)
    {
        _PauseMenuContainer.SetActive(menuToOpen == _PauseMenuContainer);
        _OptionsMenuContainer.SetActive(menuToOpen == _OptionsMenuContainer);
    }

    void OnDestroy()
    {
        _inputActions.Disable();
    }
}
