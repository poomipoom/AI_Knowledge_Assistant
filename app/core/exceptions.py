from fastapi import HTTPException, status

class DocumentProcessingError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class VectorStoreError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class NotFoundException(HTTPException):
    def __init__(self, item_name: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=f"{item_name} not found")
