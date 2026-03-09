"""
Test Script for Social Media Poster
====================================
Quick test and demo of the social media posting system.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from social_poster import (
    generate_linkedin_post,
    generate_twitter_post,
    generate_facebook_post,
    generate_instagram_caption,
    save_post_for_approval,
    run_social_posting_pipeline
)


def test_content_generation():
    """Test content generation for all platforms"""
    print("=" * 60)
    print("TESTING CONTENT GENERATION")
    print("=" * 60)

    topic = "AI and the Future of Work"

    print("\n1. LinkedIn Post:")
    print("-" * 60)
    linkedin_content = generate_linkedin_post(topic)
    print(linkedin_content)

    print("\n2. Twitter Post:")
    print("-" * 60)
    twitter_content = generate_twitter_post(topic)
    print(twitter_content)
    print(f"Character count: {len(twitter_content)}")

    print("\n3. Facebook Post:")
    print("-" * 60)
    facebook_content = generate_facebook_post(topic)
    print(facebook_content)

    print("\n4. Instagram Caption:")
    print("-" * 60)
    instagram_content = generate_instagram_caption(topic)
    print(instagram_content)

    print("\n" + "=" * 60)
    print("CONTENT GENERATION TEST COMPLETE")
    print("=" * 60)


def test_save_for_approval():
    """Test saving posts for approval"""
    print("\n" + "=" * 60)
    print("TESTING SAVE FOR APPROVAL")
    print("=" * 60)

    topic = "Test Topic"

    # Generate and save LinkedIn post
    content = generate_linkedin_post(topic)
    filepath = save_post_for_approval('linkedin', content, {'topic': topic, 'test': True})
    print(f"\n✓ Saved LinkedIn post: {filepath}")

    # Generate and save Twitter post
    content = generate_twitter_post(topic)
    filepath = save_post_for_approval('twitter', content, {'topic': topic, 'test': True})
    print(f"✓ Saved Twitter post: {filepath}")

    print("\n" + "=" * 60)
    print("SAVE FOR APPROVAL TEST COMPLETE")
    print("=" * 60)


def demo_full_pipeline():
    """Demo the full posting pipeline"""
    print("\n" + "=" * 60)
    print("DEMO: FULL POSTING PIPELINE")
    print("=" * 60)

    topic = input("\nEnter a topic for your posts: ").strip()
    if not topic:
        topic = "Innovation in Technology"

    print("\nSelect platforms (comma-separated):")
    print("Options: linkedin, twitter, facebook, instagram")
    platforms_input = input("Platforms [all]: ").strip()

    if platforms_input:
        platforms = [p.strip().lower() for p in platforms_input.split(',')]
    else:
        platforms = ['linkedin', 'twitter', 'facebook', 'instagram']

    # Run the pipeline
    run_social_posting_pipeline(topic, platforms=platforms, auto_post=False)


def quick_generate():
    """Quick generate posts without posting"""
    print("\n" + "=" * 60)
    print("QUICK GENERATE MODE")
    print("=" * 60)

    topic = input("\nEnter topic: ").strip()
    if not topic:
        print("No topic provided. Exiting.")
        return

    print("\nGenerating posts for all platforms...")

    # LinkedIn
    linkedin = generate_linkedin_post(topic)
    linkedin_file = save_post_for_approval('linkedin', linkedin, {'topic': topic})
    print(f"✓ LinkedIn: {linkedin_file.name}")

    # Twitter
    twitter = generate_twitter_post(topic)
    twitter_file = save_post_for_approval('twitter', twitter, {'topic': topic})
    print(f"✓ Twitter: {twitter_file.name}")

    # Facebook
    facebook = generate_facebook_post(topic)
    facebook_file = save_post_for_approval('facebook', facebook, {'topic': topic})
    print(f"✓ Facebook: {facebook_file.name}")

    # Instagram
    instagram = generate_instagram_caption(topic)
    instagram_file = save_post_for_approval('instagram', instagram, {'topic': topic})
    print(f"✓ Instagram: {instagram_file.name}")

    print("\n" + "=" * 60)
    print("Posts saved to: AI_Employee_Vault/Pending_Approval/")
    print("Review and approve in Obsidian, then run:")
    print("  python scripts/social_poster.py post <platform> <file>")
    print("=" * 60)


def main():
    print("""
╔══════════════════════════════════════════════════════════╗
║     SOCIAL MEDIA POSTER - TEST & DEMO SCRIPT             ║
╚══════════════════════════════════════════════════════════╝

Select an option:

1. Test Content Generation (view samples)
2. Test Save for Approval (create test files)
3. Quick Generate (generate posts for a topic)
4. Full Pipeline Demo (generate → approve → post)
5. Exit

""")

    choice = input("Enter choice [1-5]: ").strip()

    if choice == '1':
        test_content_generation()
    elif choice == '2':
        test_save_for_approval()
    elif choice == '3':
        quick_generate()
    elif choice == '4':
        demo_full_pipeline()
    elif choice == '5':
        print("\nExiting...")
        return
    else:
        print("\nInvalid choice. Exiting.")


if __name__ == "__main__":
    main()
