def format_serializer_errors(errors):
    """
    Extracts the first error message from the serializer errors.

    Args:
        errors (dict): The serializer errors dictionary.

    Returns:
        dict: A dictionary containing the formatted error message.
    """
    # Flatten the errors and extract the first message
    for field, error_list in errors.items():
        if isinstance(error_list, list) and len(error_list) > 0:
            # Extract the first error message
            first_error = error_list[0]
            if hasattr(first_error, "string"):  # Handle ErrorDetail object
                return {"message": str(first_error)}
            return {"message": str(first_error)}
    return {"message": "An unknown error occurred"}
