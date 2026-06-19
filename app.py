"""
Streamlit Web Application for Anantapur Smart City Grievance Analysis Tool
Main user interface for citizens and municipal staff
"""
import streamlit as st
import pandas as pd
from datetime import datetime
import json
from core.engine import GrievanceAnalysisEngine
from core.config import (
    APP_TITLE,
    GRIEVANCE_CATEGORIES,
    URGENCY_LEVELS,
    DEPARTMENT_MAPPING
)


# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🏙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        margin: 1rem 0;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        margin: 1rem 0;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'engine' not in st.session_state:
    st.session_state.engine = GrievanceAnalysisEngine()

if 'analysis_history' not in st.session_state:
    st.session_state.analysis_history = []

if 'system_checked' not in st.session_state:
    st.session_state.system_checked = False


def check_system_health():
    """Check and display system health"""
    health = st.session_state.engine.check_system_health()
    
    if health['status'] == 'healthy':
        st.sidebar.success("✓ System Operational")
        st.sidebar.info(f"Model: {health['model']}")
        return True
    else:
        st.sidebar.error("✗ System Degraded")
        st.sidebar.warning("Ollama server not connected")
        st.sidebar.info("Please ensure Ollama is running:\n1. `ollama serve`\n2. `ollama pull granite3-dense:8b`")
        return False


def main():
    """Main application"""
    
    # Header
    st.markdown(f'<h1 class="main-header">🏙️ {APP_TITLE}</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select Page",
        ["Submit Grievance", "Batch Analysis", "Dashboard", "About"]
    )
    
    st.sidebar.markdown("---")
    
    # System health check
    if not st.session_state.system_checked:
        st.session_state.system_healthy = check_system_health()
        st.session_state.system_checked = True
    else:
        if st.sidebar.button("🔄 Refresh System Status"):
            st.session_state.system_healthy = check_system_health()
    
    # Page routing
    if page == "Submit Grievance":
        submit_grievance_page()
    elif page == "Batch Analysis":
        batch_analysis_page()
    elif page == "Dashboard":
        dashboard_page()
    elif page == "About":
        about_page()


def submit_grievance_page():
    """Single grievance submission page"""
    st.header("📝 Submit a Grievance")
    
    if not st.session_state.system_healthy:
        st.error("⚠️ System is not operational. Please check Ollama connection.")
        return
    
    st.markdown("""
    <div class="info-box">
    <strong>Instructions:</strong>
    <ul>
        <li>Describe your grievance clearly and in detail</li>
        <li>Include location information (area, street, landmarks)</li>
        <li>Personal information will be automatically redacted for privacy</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    with st.form("grievance_form"):
        grievance_text = st.text_area(
            "Describe your grievance:",
            height=150,
            placeholder="Example: The garbage has not been collected from Gandhi Nagar, near the temple, for the past 5 days. This is causing health issues in our neighborhood."
        )
        
        citizen_id = st.text_input(
            "Citizen ID (Optional):",
            placeholder="CIT12345"
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            submit_button = st.form_submit_button("🚀 Submit & Analyze", use_container_width=True)
    
    # Process submission
    if submit_button:
        if not grievance_text.strip():
            st.error("Please enter a grievance description.")
            return
        
        with st.spinner("🔍 Analyzing your grievance..."):
            result = st.session_state.engine.analyze_grievance(
                grievance_text,
                citizen_id if citizen_id else None
            )
            
            # Add to history
            st.session_state.analysis_history.append(result)
        
        # Display results
        st.success("✅ Analysis Complete!")
        
        # Ticket Information
        st.markdown(f"""
        <div class="success-box">
        <h3>🎫 Ticket Generated</h3>
        <p><strong>Ticket ID:</strong> {result['ticket_id']}</p>
        <p><strong>Status:</strong> {result['status']}</p>
        <p><strong>Timestamp:</strong> {result['timestamp']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Analysis Results
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Category", result['category'])
            st.caption(f"Confidence: {result['classification_confidence']:.0%}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            urgency_color = {
                "Low": "🟢",
                "Medium": "🟡",
                "High": "🟠",
                "Critical": "🔴"
            }
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Urgency", f"{urgency_color.get(result['urgency_level'], '⚪')} {result['urgency_level']}")
            st.caption(f"Confidence: {result['urgency_confidence']:.0%}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Department", result['assigned_department'])
            st.caption(f"Location: {result['location']}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Detailed Information
        with st.expander("📋 Detailed Analysis"):
            st.subheader("Urgency Assessment")
            st.write(result['urgency_reasoning'])
            
            st.subheader("Location Details")
            st.write(f"**Extracted Location:** {result['location']}")
            if result['landmarks']:
                st.write(f"**Landmarks:** {', '.join(result['landmarks'])}")
            
            st.subheader("Privacy Protection")
            if result['pii_redacted']:
                st.warning(f"🔒 PII Detected and Redacted: {', '.join(result['pii_redacted'])}")
            else:
                st.success("✓ No PII detected")
            
            st.subheader("Processing Information")
            st.write(f"**Processing Time:** {result['processing_time_seconds']} seconds")
        
        # Download option
        st.download_button(
            label="📥 Download Analysis Report",
            data=json.dumps(result, indent=2),
            file_name=f"{result['ticket_id']}_report.json",
            mime="application/json"
        )


def batch_analysis_page():
    """Batch analysis page for multiple grievances"""
    st.header("📊 Batch Grievance Analysis")
    
    if not st.session_state.system_healthy:
        st.error("⚠️ System is not operational. Please check Ollama connection.")
        return
    
    st.markdown("""
    <div class="info-box">
    <strong>Upload a CSV file with grievances for batch processing.</strong><br>
    Required column: <code>text</code><br>
    Optional column: <code>citizen_id</code>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            
            if 'text' not in df.columns:
                st.error("CSV must contain a 'text' column with grievance descriptions.")
                return
            
            st.success(f"✓ Loaded {len(df)} grievances")
            st.dataframe(df.head())
            
            if st.button("🚀 Analyze All Grievances"):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                grievances = df.to_dict('records')
                results = []
                
                for i, grievance in enumerate(grievances):
                    status_text.text(f"Analyzing grievance {i+1}/{len(grievances)}...")
                    progress_bar.progress((i + 1) / len(grievances))
                    
                    result = st.session_state.engine.analyze_grievance(
                        grievance.get('text', ''),
                        grievance.get('citizen_id')
                    )
                    results.append(result)
                
                status_text.text("✅ Analysis complete!")
                
                # Store results
                st.session_state.analysis_history.extend(results)
                
                # Display statistics
                stats = st.session_state.engine.get_statistics(results)
                
                st.subheader("📈 Analysis Summary")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Grievances", stats['total_grievances'])
                with col2:
                    st.metric("Avg Processing Time", f"{stats['average_processing_time']}s")
                with col3:
                    st.metric("PII Detected", stats['total_pii_detected'])
                with col4:
                    critical_count = stats['urgency_distribution'].get('Critical', 0)
                    st.metric("Critical Issues", critical_count)
                
                # Category distribution
                st.subheader("Category Distribution")
                category_df = pd.DataFrame(
                    list(stats['category_distribution'].items()),
                    columns=['Category', 'Count']
                )
                st.bar_chart(category_df.set_index('Category'))
                
                # Results table
                st.subheader("Detailed Results")
                results_df = pd.DataFrame([{
                    'Ticket ID': r['ticket_id'],
                    'Category': r['category'],
                    'Urgency': r['urgency_level'],
                    'Department': r['assigned_department'],
                    'Location': r['location']
                } for r in results])
                st.dataframe(results_df)
                
                # Download results
                st.download_button(
                    label="📥 Download All Results",
                    data=json.dumps(results, indent=2),
                    file_name=f"batch_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
        
        except Exception as e:
            st.error(f"Error processing file: {str(e)}")


def dashboard_page():
    """Dashboard with statistics and visualizations"""
    st.header("📊 Analytics Dashboard")
    
    if not st.session_state.analysis_history:
        st.info("No grievances analyzed yet. Submit grievances to see analytics.")
        return
    
    stats = st.session_state.engine.get_statistics(st.session_state.analysis_history)
    
    # Key metrics
    st.subheader("Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Grievances", stats['total_grievances'])
    with col2:
        st.metric("Avg Processing Time", f"{stats['average_processing_time']}s")
    with col3:
        st.metric("Total PII Detected", stats['total_pii_detected'])
    with col4:
        critical = stats['urgency_distribution'].get('Critical', 0)
        st.metric("Critical Issues", critical)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Category Distribution")
        category_df = pd.DataFrame(
            list(stats['category_distribution'].items()),
            columns=['Category', 'Count']
        )
        st.bar_chart(category_df.set_index('Category'))
    
    with col2:
        st.subheader("Urgency Distribution")
        urgency_df = pd.DataFrame(
            list(stats['urgency_distribution'].items()),
            columns=['Urgency', 'Count']
        )
        st.bar_chart(urgency_df.set_index('Urgency'))
    
    # Department workload
    st.subheader("Department Workload")
    dept_df = pd.DataFrame(
        list(stats['department_workload'].items()),
        columns=['Department', 'Grievances']
    ).sort_values('Grievances', ascending=False)
    st.bar_chart(dept_df.set_index('Department'))
    
    # Recent grievances
    st.subheader("Recent Grievances")
    recent_df = pd.DataFrame([{
        'Ticket ID': g['ticket_id'],
        'Category': g['category'],
        'Urgency': g['urgency_level'],
        'Department': g['assigned_department'],
        'Timestamp': g['timestamp']
    } for g in st.session_state.analysis_history[-10:]])
    st.dataframe(recent_df)


def about_page():
    """About page with project information"""
    st.header("ℹ️ About This Tool")
    
    st.markdown("""
    ## Anantapur Smart City Grievance Analysis Tool
    
    ### 🎯 Purpose
    This AI-powered tool helps Anantapur Municipal Corporation efficiently process and route citizen grievances
    to the appropriate departments, ensuring faster resolution and better service delivery.
    
    ### 🤖 Technology
    - **AI Model:** IBM Granite (via Ollama)
    - **Framework:** Streamlit
    - **NLP:** Advanced text classification and entity extraction
    - **Privacy:** Automatic PII redaction
    
    ### 🌟 Features
    - **Automatic Classification:** Categorizes grievances into 12+ categories
    - **Urgency Assessment:** Evaluates priority based on severity and impact
    - **Smart Routing:** Assigns to appropriate municipal department
    - **Location Extraction:** Identifies affected areas and landmarks
    - **Privacy Protection:** Redacts personal information automatically
    - **Batch Processing:** Handle multiple grievances efficiently
    - **Analytics Dashboard:** Track trends and department workload
    
    ### 🎓 SDG Alignment
    **SDG 11: Sustainable Cities and Communities**
    
    This tool contributes to making Anantapur more sustainable by:
    - Improving municipal service efficiency
    - Enhancing citizen engagement
    - Enabling data-driven decision making
    - Ensuring equitable service delivery
    
    ### 👥 Target Users
    - **Citizens:** Submit and track grievances easily
    - **Municipal Staff:** Efficient grievance management
    - **Administrators:** Analytics and insights
    
    ### 📚 Responsible AI
    This tool follows responsible AI principles:
    - **Fairness:** Equal treatment for all neighborhoods
    - **Transparency:** Clear explanation of AI decisions
    - **Privacy:** PII protection and data security
    - **Ethics:** No discriminatory practices
    
    ### 📞 Support
    For technical support or feedback, contact the Anantapur Municipal Corporation IT Department.
    
    ---
    
    **Developed for:** 1M1B AI for Sustainability Virtual Internship  
    **Focus Location:** Anantapur, Andhra Pradesh  
    **Version:** 1.0.0
    """)


if __name__ == "__main__":
    main()

# Made with Bob
