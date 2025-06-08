using System.Threading.Tasks;
using DG.Tweening;
using UnityEngine;
using UnityEngine.UI;

// Manages screen transitions using fade effects
public class TransitionManager : MonoBehaviour
{
    public static TransitionManager Instance;

    [Header("Settings")]
    [SerializeField] private float duration = 1f;

    [Header("Transitions")]
    [SerializeField] private Image fadeImage;

    public enum TransitionType
    {
        FadeIn,
        FadeOut,
    }

    private async void Start()
    {
        // Start with fade in transition
        await PlayTransition(TransitionManager.TransitionType.FadeIn);
    }

    private void Awake()
    {
        Instance = this;

        // Force initial alpha value
        var color = fadeImage.color;
        color.a = 1f;
        fadeImage.color = color;
    }

    public async Task PlayTransition(TransitionType transitionType)
    {
        switch (transitionType)
        {
            case TransitionType.FadeIn:
                {
                    // Start fully opaque and fade to transparent
                    fadeImage.raycastTarget = true;
                    fadeImage.DOFade(1, 0);
                    await fadeImage.DOFade(0, duration).OnComplete(() => fadeImage.raycastTarget = false).AsyncWaitForCompletion();
                    break;
                }

            case TransitionType.FadeOut:
                {
                    // Start transparent and fade to opaque
                    fadeImage.raycastTarget = true;
                    fadeImage.DOFade(0, 0);
                    await fadeImage.DOFade(1, duration)
                        .OnComplete(() => fadeImage.raycastTarget = true)
                        .AsyncWaitForCompletion();
                    break;
                }

            default:
                break;
        }
    }
}
