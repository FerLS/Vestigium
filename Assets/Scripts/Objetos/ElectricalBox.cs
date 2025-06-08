using UnityEngine;
using UnityEngine.UI;

public class SwitchManager : Interactable
{
    public Button[] switches;
    public Sprite spriteOn, spriteOff;
    private bool[] states = new bool[8];

    [SerializeField] private GameObject canvas;

    // Defines which switches affect other switches when toggled
    private int[][] dependencies = new int[][]
    {
        new int[] {1, 2},
        new int[] {0, 3},
        new int[] {4},
        new int[] {5},
        new int[] {6},
        new int[] {},
        new int[] {7},
        new int[] {2}
    };

    protected override void Start()
    {
        base.Start();
        // All switches start ON (true)
        for (int i = 0; i < states.Length; i++)
            states[i] = true;

        for (int i = 0; i < switches.Length; i++)
        {
            int index = i;
            switches[i].onClick.AddListener(() => ToggleSwitch(index));
            UpdateVisual(index);
        }
    }

    void ToggleSwitch(int index)
    {
        states[index] = !states[index];

        // Toggle dependent switches
        foreach (int affected in dependencies[index])
        {
            states[affected] = !states[affected];
            UpdateVisual(affected);
        }

        UpdateVisual(index);

        // Check if all switches are OFF to win
        if (CheckWin())
        {
            Destroy(canvas);

            foreach (Light light in GetComponentsInChildren<Light>(includeInactive: true))
            {
                light.enabled = false;
            }
            foreach (ParticleSystem particle in GetComponentsInChildren<ParticleSystem>(includeInactive: true))
            {
                particle.Stop();
            }
            PlayerController.Instance.EnableControls();
            enabled = false;
        }
    }

    void UpdateVisual(int index)
    {
        Image img = switches[index].GetComponent<Image>();
        img.sprite = states[index] ? spriteOn : spriteOff;
    }

    // Returns true if all switches are OFF
    bool CheckWin()
    {
        foreach (bool s in states)
            if (s) return false;
        return true;
    }

    public override void OnStartInteraction()
    {
        canvas.SetActive(true);
        PlayerController.Instance.DisableControls();
    }

    public override void OnStopInteraction()
    {
    }
}
