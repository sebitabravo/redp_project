import os
import django

# Configurar Django para usar los modelos
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Directorio base del proyecto
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf.settings')  # Cambia 'drf' si es el nombre correcto de tu proyecto
os.chdir(BASE_DIR)  # Cambia al directorio base del proyecto
django.setup()

from api.models import Experience, User, Category

def show_menu():
    print("\nCRUD Experience Menu:")
    print("1. Create Experience")
    print("2. Read Experiences")
    print("3. Update Experience")
    print("4. Delete Experience")
    print("5. Exit")
    return input("Choose an option: ")

def create_experience():
    try:
        title = input("Enter title: ")
        category = input("Enter category (food, milestone, culture): ")
        description = input("Enter description: ")
        rating = int(input("Enter rating (1-5): "))
        additional_info = input("Enter additional info (JSON format or leave blank): ")
        user_email = input("Enter user email: ")

        # Validar si el usuario existe
        try:
            user = User.objects.get(email=user_email)
        except User.DoesNotExist:
            print(f"Error: User with email {user_email} does not exist.")
            return

        experience = Experience.objects.create(
            title=title,
            category=category,
            description=description,
            rating=rating,
            additional_info=additional_info or None,
            user=user
        )
        print(f"Experience '{experience.title}' created successfully!")
    except Exception as e:
        print(f"Error creating experience: {e}")

def read_experiences():
    try:
        experiences = Experience.objects.all()
        if not experiences:
            print("No experiences found.")
        for exp in experiences:
            print(f"ID: {exp.id}, Title: {exp.title}, Category: {exp.get_category_display()}, "
                  f"Description: {exp.description}, Rating: {exp.rating}, User: {exp.user.email}")
    except Exception as e:
        print(f"Error reading experiences: {e}")

def update_experience():
    try:
        experience_id = int(input("Enter the ID of the experience to update: "))
        experience = Experience.objects.get(pk=experience_id)

        print("Leave a field blank to keep the current value.")
        title = input(f"Enter new title (current: {experience.title}): ") or experience.title
        category = input(f"Enter new category (current: {experience.category}): ") or experience.category
        description = input(f"Enter new description (current: {experience.description}): ") or experience.description
        rating = input(f"Enter new rating (current: {experience.rating}): ")
        additional_info = input(f"Enter new additional info (current: {experience.additional_info}): ") or experience.additional_info

        experience.title = title
        experience.category = category
        experience.description = description
        experience.rating = int(rating) if rating else experience.rating
        experience.additional_info = additional_info
        experience.save()

        print(f"Experience '{experience.title}' updated successfully!")
    except Experience.DoesNotExist:
        print("Experience not found.")
    except Exception as e:
        print(f"Error updating experience: {e}")

def delete_experience():
    try:
        experience_id = int(input("Enter the ID of the experience to delete: "))
        experience = Experience.objects.get(pk=experience_id)
        experience.delete()
        print(f"Experience '{experience.title}' deleted successfully!")
    except Experience.DoesNotExist:
        print("Experience not found.")
    except Exception as e:
        print(f"Error deleting experience: {e}")

def main():
    while True:
        choice = show_menu()
        if choice == "1":
            create_experience()
        elif choice == "2":
            read_experiences()
        elif choice == "3":
            update_experience()
        elif choice == "4":
            delete_experience()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
