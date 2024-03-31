
        else:
            return None

    except Exception:
        # fe.server_contact_error()
        values = {"name":name,"contact": user_contact}
        session[session_var] = values  
        return redirect(path) 