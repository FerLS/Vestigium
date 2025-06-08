using UnityEngine;

public class CatWalk : MonoBehaviour
{
    public Transform destination; // Target destination for the cat
    public float speed = 3f;

    private Animator animator;
    private bool isActive = false;

    [Header("Audio")]
    [SerializeField] private AudioClip licking;
    [SerializeField] private AudioClip eating;

    [SerializeField] private GameObject catSat; // Cat in sitting position

    void Start()
    {
        animator = GetComponent<Animator>();
        gameObject.SetActive(false);
        // Start the licking sound loop when initialized
        AudioManager.Instance.PlayLoopSFX3D("licking", licking, catSat.transform);
    }

    public void Activate()
    {
        catSat.SetActive(false);
        AudioManager.Instance.StopLoopSound("licking");
        gameObject.SetActive(true);
        animator.SetTrigger("Run");
        isActive = true;
    }

    void Update()
    {
        if (!isActive) return;

        // Move cat toward destination
        float step = speed * Time.deltaTime;
        transform.position = Vector3.MoveTowards(transform.position, destination.position, step);

        // Rotate cat to face destination
        Vector3 dir = destination.position - transform.position;
        dir.y = 0;
        if (dir != Vector3.zero)
            transform.rotation = Quaternion.Slerp(transform.rotation, Quaternion.LookRotation(dir), 5 * Time.deltaTime);

        // Check if cat has reached the destination
        if (Vector3.Distance(transform.position, destination.position) < 2.5f)
        {
            animator.SetTrigger("Stop");
            AudioManager.Instance.PlayLoopSFX3D("eating", eating, transform);
            isActive = false;
        }
    }
}
