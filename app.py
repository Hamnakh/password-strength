import streamlit as st
import re

def calculate_password_strength(password):
    strength = 0
    suggestions = []

    # Length check
    if len(password) >= 8:
        strength += 25
    else:
        suggestions.append("Password should be at least 8 characters long")

    # Check for uppercase letters
    if re.search(r'[A-Z]', password):
        strength += 25
    else:
        suggestions.append("Add uppercase letters")

    # Check for lowercase letters
    if re.search(r'[a-z]', password):
        strength += 25
    else:
        suggestions.append("Add lowercase letters")

    # Check for numbers
    if re.search(r'[0-9]', password):
        strength += 15
    else:
        suggestions.append("Add numbers")

    # Check for special characters
    if re.search(r'[^A-Za-z0-9]', password):
        strength += 10
    else:
        suggestions.append("Add special characters")

    return strength, suggestions

def get_strength_color(strength):
    if strength < 30:
        return "#ff4b4b"  # Red
    elif strength < 50:
        return "#ffa500"  # Orange
    elif strength < 75:
        return "#ffd700"  # Yellow
    else:
        return "#4caf50"  # Green

def get_strength_label(strength):
    if strength < 30:
        return "Very Weak"
    elif strength < 50:
        return "Weak"
    elif strength < 75:
        return "Moderate"
    else:
        return "Strong"

def main():
    st.set_page_config(page_title="Password Strength Meter", page_icon="🔒", layout="centered")

    # Custom CSS for styling
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            background-color: #2a2a2a;
            color: white;
            border-radius: 5px;
            padding: 10px;
        }
        .password-strength {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
            text-align: center;
            font-weight: bold;
        }
        .suggestions {
            padding: 10px;
            border-radius: 5px;
            background-color: #2a2a2a;
            color: white;
            margin: 10px 0;
        }
        .requirements {
            padding: 10px;
            border-radius: 5px;
            background-color: #2a2a2a;
            color: white;
            margin: 10px 0;
        }
        .requirements ul {
            list-style-type: none;
            padding: 0;
        }
        .requirements li {
            margin: 5px 0;
        }
        .requirements li.valid {
            color: #4caf50;
        }
        .requirements li.invalid {
            color: #ff4b4b;
        }
        </style>
    """, unsafe_allow_html=True)

    # Title
    st.title("🔒 Password Strength Meter")
    st.markdown("### Check how strong your password is!")

    # Create two columns for password input and show/hide toggle
    col1, col2 = st.columns([4, 1])
    
    # Add show/hide password toggle in session state if it doesn't exist
    if 'show_password' not in st.session_state:
        st.session_state.show_password = False

    # Password input with show/hide functionality
    with col1:
        password = st.text_input(
            "Enter your password",
            type="password",
            placeholder="Enter your password"
        )

    # Show/Hide toggle button
    with col2:
        if st.button(
            "👁️ Show" if not st.session_state.show_password else "👁️ Hide",
            help="Toggle password visibility"
        ):
            st.session_state.show_password = not st.session_state.show_password

    # Display current password (if show is enabled)
    if st.session_state.show_password and password:
        st.info(f"Current password: {password}")

    if password:
        strength, suggestions = calculate_password_strength(password)
        
        # Display strength meter
        st.progress(strength / 100)
        
        # Display strength label with color
        strength_color = get_strength_color(strength)
        strength_label = get_strength_label(strength)
        st.markdown(
            f"<div class='password-strength' style='background-color: {strength_color};'>"
            f"Password Strength: {strength_label} ({strength}%)</div>",
            unsafe_allow_html=True
        )

        # Display suggestions if any
        if suggestions:
            st.markdown("### Suggestions for improvement:")
            st.markdown("<div class='suggestions'>" + "<br>".join(suggestions) + "</div>", unsafe_allow_html=True)

        # Password requirements
        st.markdown("### Password Requirements:")
        st.markdown("""
            <div class='requirements'>
                <ul>
                    <li class='{}'>Minimum 8 characters</li>
                    <li class='{}'>Uppercase letters</li>
                    <li class='{}'>Lowercase letters</li>
                    <li class='{}'>Numbers</li>
                    <li class='{}'>Special characters</li>
                </ul>
            </div>
        """.format(
            "valid" if len(password) >= 8 else "invalid",
            "valid" if re.search(r'[A-Z]', password) else "invalid",
            "valid" if re.search(r'[a-z]', password) else "invalid",
            "valid" if re.search(r'[0-9]', password) else "invalid",
            "valid" if re.search(r'[^A-Za-z0-9]', password) else "invalid"
        ), unsafe_allow_html=True)

if __name__ == "__main__":
    main()