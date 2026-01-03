def list_courses(service):
    """Fetches all active courses."""
    courses = []
    page_token = None
    while True:
        response = service.courses().list(pageSize=100, pageToken=page_token).execute()
        courses.extend(response.get('courses', []))
        page_token = response.get('nextPageToken', None)
        if not page_token:
            break
    return courses

def get_files_from_course(service, course_id):
    """Scans Assignments, Materials, and Announcements for Drive files."""
    files_found = []

    def extract_from_items(items, source_type):
        extracted = []
        if not items: return extracted
        for item in items:
            # Use post title, or truncate text if it's an announcement
            post_title = item.get('title') or item.get('text', 'Unknown Post')[:30]
            
            if 'materials' in item:
                for material in item['materials']:
                    if 'driveFile' in material:
                        df = material['driveFile']['driveFile']
                        extracted.append({
                            'id': df['id'],
                            'title': df['title'],
                            'source': source_type,
                            'post_title': post_title
                        })
        return extracted

    # 1. Assignments
    print(" - Scanning Assignments...")
    cw = service.courses().courseWork().list(courseId=course_id).execute()
    files_found.extend(extract_from_items(cw.get('courseWork', []), "Assignment"))

    # 2. Materials
    print(" - Scanning Materials...")
    try:
        cwm = service.courses().courseWorkMaterials().list(courseId=course_id).execute()
        files_found.extend(extract_from_items(cwm.get('courseWorkMaterial', []), "Material"))
    except: pass

    # 3. Announcements
    print(" - Scanning Stream...")
    try:
        ann = service.courses().announcements().list(courseId=course_id).execute()
        files_found.extend(extract_from_items(ann.get('announcements', []), "Stream"))
    except: pass

    return files_found