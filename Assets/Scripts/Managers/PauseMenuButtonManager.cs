using UnityEngine;

public class PauseMenuButtonManager : MonoBehaviour
{
    // Type of pause menu button this component represents
    [SerializeField] private PauseMenuManager.PauseMenuButtons _buttonType;

    // Called when this button is clicked
    public void ButtonClicked()
    {
        PauseMenuManager._.PauseMenuButtonClicked(_buttonType);
    }
}
