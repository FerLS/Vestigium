using UnityEngine;

/// <summary>
/// Handles button click events in the main menu
/// </summary>
public class MainMenuButtonManager : MonoBehaviour
{
    // Button type from MainMenuManager enum
    [SerializeField] private MainMenuManager.MainMenuButtons _buttonType;

    /// <summary>
    /// Called when this button is clicked
    /// </summary>
    public void ButtonClicked()
    {
        // Notify the MainMenuManager singleton
        MainMenuManager._.MainMenuButtonClicked(_buttonType);
    }
}
