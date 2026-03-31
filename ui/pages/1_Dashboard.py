import streamlit as st
import sys
from pathlib import Path
from job_tracker.tracking.database import init_db, get_all_applications, update_status, delete_application

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
init_db()

st.title("Application Dashboard")
apps = get_all_applications()

if not apps:
    st.info("No applications yet. Go to 'Add Job' to add your first one!")
else:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", len(apps))
    col2.metric("Applied", sum(1 for a in apps if a["status"] == "applied"))
    col3.metric("Interviews", sum(1 for a in apps if a["status"] == "interview"))
    col4.metric("Offers", sum(1 for a in apps if a["status"] == "offer"))

    st.markdown("---")

    for app in apps:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 1])

            with col1:
                st.markdown(f"**{app['company']}** - {app['role']}")
                if app.get("location"):
                    st.caption(f" {app['location']}")

            with col2:
                status_colors = {
                    "saved": "🔵", "applied": "🟡", "interview": "🟢",
                    "rejected": "🔴", "offer": "⭐", "accepted": "🏅"
                }
                st.markdown(f"{status_colors.get(app['status'], '')} {app['status'].upper()}")

            with col3:
                if app.get("match_score"):
                    st.markdown(f"Match: **{app['match_score']:.0f}%**")
                if app.get("salary_range"):
                    st.caption(f" 🤑 {app['salary_range']}")

            with col4:
                new_status = st.selectbox(
                    "Update",
                    ["saved", "applied", "interview", "rejected", "offer", "accepted"],
                    index=["saved", "applied", "interview", "rejected", "offer", "accepted"].index(app["status"]),
                    key=f"status_{app['id']}"
                )
                if new_status != app["status"]:
                    update_status(app["id"], new_status)
                    st.rerun()

            with col5:
                if st.button("❌", key=f"delete_{app['id']}", help="Delete this application"):
                    st.session_state[f"confirm_delete_{app['id']}"] = True
                
            if st.session_state.get(f"confirm_delete_{app['id']}", False):
                st.warning(f"Are you sure you want to delete **{app['company']} - {app['role']}**?")
                col_yes, col_no, _= st.columns([1, 1, 4])
                with col_yes:
                    if st.button("Yes, delete", key=f"yes_{app['id']}", type="primary"):
                        delete_application(app["id"])
                        del st.session_state[f"confirm_delete_{app['id']}"]
                        st.rerun()
                with col_no:
                    if st.button("Cancel", key=f"no_{app['id']}", type="primary"):
                        del st.session_state[f"confirm_delete_{app['id']}"]
                        st.rerun()
            
            st.markdown("---")