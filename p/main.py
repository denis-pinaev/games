from router import Router

if __name__ == "__main__":
    Router.send(Router.State.initial_clean_old_files)
    """
    if you already have ZIP files for test you can run:
    Router.send(Router.State.extract_zip_files)
    """