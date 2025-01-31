from fastapi import HTTPException, status
from sqlalchemy import desc
from app.core import utilities
from app.core import oauth2
from app.models import auth_model
from app.schemas import audit_trail_schema, auth_schema
from sqlalchemy.orm import Session
from app.core.route_name import admin1, admin2
from app.services.audit_trail_service import createAuditTrail


def userLogin(payload: auth_schema.UserLogin, db: Session):
    exist_user = db.query(auth_model.User).filter(
            auth_model.User.email == payload.email).first()
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with this {payload.email} invalid')
        
    # Verify password
    if not utilities.verify(payload.password, exist_user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Incorrect password')
    
    # Generate access token
    accessToken = oauth2.createAccessToken(data={"user_id": exist_user.id})
    data = auth_schema.Token(access_token=accessToken, name=exist_user.name, role=exist_user.role).model_dump()
    
    # Remove password securely
    exist_user.password = None
    
    # Commit changes to the database
    db.commit()
    return data



def sendOtp(payload: auth_schema.SendPassword, db: Session):
    exist_user = db.query(auth_model.User).filter(
        auth_model.User.email == payload.email)
    user = exist_user.first()
    if not user and not (payload.email==admin1 or payload.email == admin2):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with this {payload.email} invalid')

    if not user and payload.email==admin1:
        #send password
        password_sent = utilities.sendPasswordSmtp(payload.email)
        if not password_sent:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Failed to send password to this email {payload.email}')
        #create user
        hashedPassword = utilities.hashedPassword(password_sent)
        admin_user = auth_schema.UserCreate(email=payload.email, password=hashedPassword, role=0, name="Soton Ahmed")
        admin = auth_model.User(**admin_user.model_dump())
        db.add(admin)
        db.commit()
        db.refresh(admin)

    if not user and payload.email == admin2:
        #send password
        password_sent = utilities.sendPasswordSmtp(payload.email)
        if not password_sent:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Failed to send password to this email {payload.email}')
        #create user
        hashedPassword = utilities.hashedPassword(password_sent)
        admin_user = auth_schema.UserCreate(email=payload.email, password=hashedPassword, role=0, name="Shamol Kumar Das")
        admin = auth_model.User(**admin_user.model_dump())
        db.add(admin)
        db.commit()
        db.refresh(admin)
    
    #send password
    password_sent = utilities.sendPasswordSmtp(payload.email)
    if not password_sent:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Failed to send password to this email {payload.email}')
    #update user password
    hashedPassword = utilities.hashedPassword(password_sent)
    user.password = hashedPassword
    db.commit()



def userCreate(payload: auth_schema.UserCreate, db: Session, current_user: auth_model.User):
    #check user role
    if current_user.role > 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'You are not eligible to create users')
    #check already exist
    exist_user = db.query(auth_model.User).filter(
        auth_model.User.email == payload.email).first()
    
    if exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Already exist with this {payload.email} email')
        
    new_user = auth_schema.UserCreate(email=payload.email, role=payload.role, created_by=current_user.email, name=payload.name)
    userDump = auth_model.User(**new_user.model_dump())
    db.add(userDump)
    audit_payload = audit_trail_schema.AuditTrailCreate(task_by=current_user.email, task= "Create", sector='User',impact=payload.email)
    createAuditTrail(payload=audit_payload, db=db)
    db.commit()
    db.refresh(userDump)


def allUser(db: Session):
    users = db.query(auth_model.User).order_by(desc(auth_model.User.created_at)).all()
    users_data = [auth_schema.UserOut.model_validate(
            user).model_dump() for user in users]
    return users_data
            


def userDelete(user_id: int, db: Session, current_user: auth_model.User):
    #check user role
    if current_user.role > 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You are not eligible to delete users')
    
    #can't delete own
    if current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You cannot delete yourself')
    
    #check already exist
    exist_user = db.query(auth_model.User).filter(
        auth_model.User.id == user_id)
    if not exist_user.first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User not found with this id ({user_id})')

    exist_user_email = exist_user.first().email
    exist_user.delete(synchronize_session=False)
    audit_payload = audit_trail_schema.AuditTrailCreate(task_by=current_user.email, task= "Delete", sector='User', impact=exist_user_email)
    createAuditTrail(payload=audit_payload, db=db)
    db.commit()



def userUpdate(user_id: int, payload: auth_schema.UserUpdate, db: Session , current_user: auth_model.User):
     #check user role
    if current_user.role > 1 or current_user.id == user_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='You are not eligible to update user')
    
    exist_user = db.query(auth_model.User).filter(
            auth_model.User.id == user_id).first()
        
    if not exist_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'User not found with this id ({user_id})')

    exist_user.role = payload.role
    exist_user.name = payload.name
    exist_user.updated_by = current_user.email
    audit_payload = audit_trail_schema.AuditTrailCreate(task_by=current_user.email, task= "Update",sector='User',impact=exist_user.email)
    createAuditTrail(payload=audit_payload, db=db)
    db.commit()