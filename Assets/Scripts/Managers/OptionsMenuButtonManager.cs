using UnityEngine;

public class OptionsMenuButtonManager : MonoBehaviour
{
    // Button type to use when in main menu
    [SerializeField] MainMenuManager.OptionsButtons _buttonTypeMainMenu;
    // Button type to use when in pause menu
    [SerializeField] PauseMenuManager.OptionsButtons _buttonTypePauseMenu;
    // Flag to determine if this is part of the pause menu
    [SerializeField] private bool _isPauseMenu;

    // Called when the button is clicked
    public void ButtonClicked()
    {
        if (_isPauseMenu) PauseMenuManager._.OptionsButtonClicked(_buttonTypePauseMenu);
        else MainMenuManager._.OptionsButtonClicked(_buttonTypeMainMenu);
    }
}
