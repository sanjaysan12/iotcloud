from flask import Flask,redirect,url_for,request,render_template,session,Blueprint,Response,send_file
from src.User import User
from src import get_config
from blueprints import home
import mimetypes
from src.Database import Database
from gridfs import GridFS, GridFSBucket
import uuid
bp = Blueprint("files",__name__,url_prefix="/files")
db = Database.get_connection()
def guess_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    
    if mime_type is None:
        extension = filename.split('.')[-1].lower()
        # Fallback MIME types based on file extensions
        extension_map = {
            'pdf': 'application/pdf',
            'txt': 'text/plain',
            'html': 'text/html',
            'jpg': 'image/jpeg',
            'png': 'image/png',
            'csv': 'text/csv',
            'json': 'application/json'
        }
        mime_type = extension_map.get(extension, 'application/octet-stream')
    
    return mime_type

@bp.route('/upload/bucket',methods=['POST'])
def upload():
    if 'file' in request.files and session.get('authenticated'):
        file = request.files['file']
        fs = GridFSBucket(db)
        filename = str(uuid.uuid4())
        metadata = {
            'original_filename':file.filename,
            'content_type': guess_mime_type(file.filename),
            'owner': session.get('username')
        }
        fileid=fs.upload_from_stream(filename,file,metadata=metadata)
        return  {
            'message': 'upload success',
            'file_id':str(fileid),
            'filename':filename,
            'download_url':'/files/bucket/get/'+filename,
            'type' : 'success'
        },200
    else:
        return {
            'message':'Bad request',
            'type':'Error'
        },400
        
@bp.route('/put',methods=['POST'])  
def fs_put():
    if 'file' in request.files and session.get('authenticated'):
        fs = GridFS(db)
        file = request.files['file']
        filename = str(uuid.uuid4())
        metadata = {
            'original_filename':file.filename,
            'content_type': guess_mime_type(file.filename),
            'owner': session.get('username')
            
        }
        fileid = fs.put(file,filename=filename,content_type=guess_mime_type(file.filename),original_filename = file.filename,test = "just for fun",metadata=metadata)
        return  {
            'message': 'upload success',
            'file_id':str(fileid),
            'filename':filename,
            'download_url':'/files/bucket/get/'+filename,
            'type' : 'success'
        },200
    else:
         return {
            'message':'Bad request',
            'type':'Error'
        },400
        
       
@bp.route('/bucket/get/<filename>',methods=['GET'])
def get_bucket(filename):
    if session.get('authenticated'):
        try:
            fs = GridFSBucket(db)
            file = fs.open_download_stream_by_name(filename)
            response = Response(file.read(),status=200,mimetype=file.metadata['content_type'])
            return response
        except:
            return {
                'message': 'file not found',
                'type':'error',        
            },404
    else:
        return {
            'message':'Bad Request',
            'type':'error'
        }
        
@bp.route('/download/<filename>',methods=['GET'])
def get_fs(filename):
    if session.get('authenticated'):
        try:
            fs = GridFS(db)
            file = fs.find_one(
                {
                    'filename':filename
                }
            )
            if file is None:
                 return {
                'message': 'file not found',
                'type':'error',        
            },404
            download_name=file.metadata['original_filename']
            return send_file(file,mimetype=file.metadata['content_type'],as_attachment=True,download_name=download_name)
        except:
             return {
                'message': 'file not found',
                'type':'error',        
            },404
    else:
        return {
            'message':'Bad Request',
            'type':'error'
        }
    
@bp.route('/stream/<filename>', methods=['GET'])
def stream_fs(filename):
    db = Database.get_connection()
    file_doc = db.fs.files.find_one({
        'filename': filename
    })
    
    if file_doc is None:
         return {
                'message': 'File not found',
                'type': 'error'
            }, 404
    
    total_size = file_doc['length']
    chunk_size = file_doc['chunkSize']
    mime_type = file_doc['metadata']['content_type']
    
    range_header = request.headers.get('Range', None)
    if not range_header:
        start = 0
        end = chunk_size - 1
    else:
        range_bytes = range_header.split("=")[1]
        range_split = range_bytes.split("-")
        start = int(range_split[0])
        end = int(range_split[1])
        
    start_chunk = start // chunk_size
    end_chunk = end // chunk_size
    
    def stream():
        for chunk_number in range(start_chunk, end_chunk + 1): # +1 because range is exclusive
            chunk = db.fs.chunks.find_one({
                'files_id': file_doc['_id'],
                'n': chunk_number
            })
            start_index = max(0, start - (chunk_number * chunk_size))
            end_index = min(chunk_size, end - (chunk_number * chunk_size) + 1)
            yield chunk['data'][start_index:end_index]
            
    response = Response(stream(), status=206, mimetype=mime_type, direct_passthrough=True)
    response.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, end, total_size))
    response.headers.add('Accept-Ranges', 'bytes')
    
    return response
