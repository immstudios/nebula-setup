__all__ = ["META_TYPES"]

STRING       = 0       # Single-line plain text (default)
TEXT         = 1       # Multiline text. 'syntax' can be provided in config
INTEGER      = 2       # Integer only value (for db keys etc)
NUMERIC      = 3       # Any integer of float number. 'min', 'max' and 'step' values can be provided in config
BOOLEAN      = 4       # 1/0 checkbox
DATETIME     = 5       # Date and time information. Stored as timestamp
TIMECODE     = 6       # Timecode information, stored as float(seconds), presented as HH:MM:SS:FF or HH:MM:SS.CS (centiseconds)
REGIONS      = 7
FRACTION     = 8       # 16/9 etc. Stored as string
SELECT       = 9
LIST         = 10
COLOR        = 11


META_TYPES = {

# KEY                       NS   E  I  F  CLASS        SETTINGS


"id":                     ("o",  0, 1, 0, INTEGER,     None),
"id_asset":               ("o",  0, 1, 0, INTEGER,     None),
"id_item":                ("o",  0, 1, 0, INTEGER,     None),
"id_bin":                 ("o",  0, 1, 0, INTEGER,     None),
"id_event":               ("o",  0, 1, 0, INTEGER,     None),
"id_user":                ("o",  0, 1, 0, INTEGER,     None),


"ctime":                  ("o",  0, 0, 0, DATETIME,    None),              # Creation time
"mtime":                  ("o",  0, 0, 0, DATETIME,    None),              # Last modified time

"is_admin":               ("u",  1, 0, 0, BOOLEAN,     None),              # User has admin privileges
"full_name":              ("u",  1, 0, 0, STRING,      None),              # Full name of the user

"start":                  ("e",  1, 0, 0, DATETIME,    None),              # Event start time
"stop":                   ("e",  1, 0, 0, DATETIME,    None),
"run_mode":               ("ei", 0, 0, 0, INTEGER,     None),
"loop":                   ("i" , 0, 0, 0, BOOLEAN,     None),
"rundown_broadcast":      ("v",  0, 0, 0, DATETIME,    {"format" : "%H:%M:%S"}),
"rundown_scheduled":      ("v",  0, 0, 0, DATETIME,    {"format" : "%H:%M:%S"}),
"rundown_difference":     ("v",  0, 0, 0, TIMECODE,    None),
"rundown_symbol":         ("v",  0, 0, 0, INTEGER,     None),
"rundown_row":            ("v",  0, 0, 0, INTEGER,     None),
"is_empty":               ("v",  0, 0, 0, BOOLEAN,     None),

"solver":                 ("ai", 1, 0, 0, SELECT,      {"cs" : "urn:site:solvers"}),
"mark_in":                ("ai", 1, 0, 0, TIMECODE,    None),
"mark_out":               ("ai", 1, 0, 0, TIMECODE,    None),
"logo":                   ("ai", 1, 0, 0, SELECT,      {"cs" : "urn:site:logo"}),

#
# Asset specific
#

"media_type":             ("a", 0, 0, 0, INTEGER,     None),
"content_type":           ("a", 0, 0, 0, INTEGER,     None),
"status":                 ("a", 0, 0, 0, INTEGER,     {"default" : 1}),              # OFFLINE, ONLINE, CREATING, TRASHED, ARCHIVED
"version_of":             ("a", 0, 0, 0, INTEGER,     {"default" : 0}),
"id_storage":             ("a", 0, 1, 0, INTEGER,     None),
"id_folder":              ("a", 0, 0, 0, INTEGER,     None),
"path":                   ("a", 0, 0, 1, STRING,      None),
"subclips":               ("a", 1, 0, 0, REGIONS,     None),
"article":                ("a", 1, 0, 1, TEXT,        {"mode" : "rich"}),
"cue_sheet":              ("a", 1, 0, 1, TEXT,        None),
"aired":                  ("a", 1, 0, 0, BOOLEAN,     None),

#
# Descriptive
#
# If id_folder  is changed and "m" key is not specified in the asset type settings, existing values are deleted
#

#                               E  I  F
"title":                  ("m", 1, 0, 9, STRING,      None),                       # dc.title.main - The title most commonly associated with the resource.
"subtitle":               ("m", 1, 0, 8, STRING,      None),                       # dc.title.subtitle - Ancillary title information for the resource.
"description":            ("m", 1, 0, 7, TEXT,        {"syntax" : "md"}),
"color":                  ("m", 1, 0, 0, COLOR,       None),                       # Object highlight color
"notes":                  ("m", 1, 0, 1, TEXT,        None),                       # Production notes
"promoted":               ("m", 1, 0, 0, BOOLEAN,     None),                       # Asset "promotion". It"s hit, important, favourite,....

"title/original":         ("m", 1, 0, 9, STRING,      None),                       # dc.title.main - The title most commonly associated with the resource.
"subtitle/original":      ("m", 1, 0, 8, STRING,      None),                       # dc.title.subtitle - Ancillary title information for the resource.
"description/original":   ("m", 1, 0, 7, TEXT,        {"syntax" : "md"}),

"language":               ("m", 1, 1, 0, SELECT,      {"cs" : "urn:ebu:metadata-cs:ISO639_1LanguageCodeCS", "order" : "alias"}),
"editorial_format":       ("m", 1, 0, 0, SELECT,      {"cs" : "urn:ebu:metadata-cs:EditorialFormatCodeCS", "mode" : "tree"}),
"editorial_control":      ("m", 1, 0, 0, SELECT,      {"cs" : "urn:ebu:metadata-cs:EditorialControlCodeCS", "mode" : "radio"}),
"intended_audience":      ("m", 1, 0, 0, LIST,        {"cs" : "urn:ebu:metadata-cs:IntendedAudienceCodeCS", "mode" : "tree"}),
"intention":              ("m", 1, 0, 0, LIST,        {"cs" : "urn:ebu:metadata-cs:IntentionCodeCS", "mode" : "tree"}),
"genre":                  ("m", 1, 1, 0, SELECT,      {"cs" : "urn:ebu:metadata-cs:ContentGenreCS", "mode" : "tree"}),
"atmosphere":             ("m", 1, 1, 0, LIST,        {"cs" : "urn:tva:metadata-cs:AtmosphereCS", "order" : "alias"}),
"place":                  ("m", 1, 1, 0, LIST,        {"cs" : "urn:tva:metadata-cs:PlaceTypeCS", "mode" : "tree"}),

"origination":            ("m", 1, 0, 0, SELECT,      {"cs" : "urn:tva:metadata:cs:OriginationCS", "mode" : "tree"}),
"content_alert":          ("m", 1, 0, 0, LIST,        {"cs" : "urn:tva:metadata-cs:ContentAlertCS", "mode" : "tree"}),
"content_alert/scheme":   ("m", 1, 0, 0, SELECT,      {"cs" : "urn:ebu:metadata-cs:ContentAlertSchemeCodeCS", "mode" : "tree"}),
"graphic_usage":          ("m", 1, 0, 0, SELECT,      {"cs" : "urn:ebu:metadata-cs:GraphicUsageTypeCodeCS"}),
"keywords":               ("m", 1, 0, 9, STRING,      None),                       # Comma delimited keywords list

"year":                   ("m", 1, 0, 0, INTEGER,     {"hide_null" : True}),
"date":                   ("m", 1, 0, 0, DATETIME,    {"mode" : "date"}),
"date/valid":             ("m", 1, 0, 0, DATETIME,    {"mode" : "date"}),
"date/valid/ott":         ("m", 1, 0, 0, DATETIME,    {"mode" : "date"}),

"rights":                 ("m", 1, 0, 0, SELECT,      {"cs" : "urn:immstudios:metadata-cs:ContentLicenceCS"}),
"rights/type":            ("m", 1, 0, 0, LIST,        {"cs" : "urn:ebu:metadata-cs:RightTypeCodeCS"}),
"rights/attribution":     ("m", 1, 0, 1, STRING,      None),
"rights/attribution/url": ("m", 1, 0, 1, STRING,      None),
"rights/description":     ("m", 1, 0, 1, TEXT,        None),
"rights/ott":             ("m", 1, 0, 0, BOOLEAN,     None),
"rights/spatial":         ("m", 1, 0, 0, SELECT,      {"cs" : "urn:site:rights-spatial"}),

"source":                 ("m", 0, 0, 1, STRING,      None),                       # Youtube, Vimeo, PirateBay....
"source/url":             ("m", 0, 0, 1, STRING,      None),
"source/attribution":     ("m", 0, 0, 1, STRING,      None),                       # DEPRECATED
"source/rating":          ("m", 0, 1, 0, INTEGER,     None),                       # Provided rating normalized to: from 0 (worst) to 100 (best)

"commercial/content":     ("m", 1, 0, 0, SELECT,      {"cs" : "urn:tva:metadata-cs:ContentCommercialCS", "mode" : "tree"}),
"commercial/campaign":    ("m", 1, 0, 0, INTEGER,     None),                       # Campaign event id
"commercial/client":      ("m", 1, 0, 0, SELECT,      {"cs" : "urn:site:clients"}),

"runs/daily":             ("m", 1, 0, 0, INTEGER,     None),
"runs/weekly":            ("m", 1, 0, 0, INTEGER,     None),
"runs/monthly":           ("m", 1, 0, 0, INTEGER,     None),
"runs/total":             ("m", 1, 0, 0, INTEGER,     None),

"album":                  ("m", 1, 0, 1, STRING,      None),
"serie":                  ("m", 1, 0, 1, SELECT,      {"cs" : "urn:site:series", "order" : "alias"}),
"serie/season":           ("m", 1, 0, 0, INTEGER,     None),
"serie/episode":          ("m", 1, 0, 0, INTEGER,     None),

"id/main":                ("m", 1, 0, 8, STRING,      None),                       # Primary Content ID (local or global)
"id/youtube":             ("m", 0, 0, 8, STRING,      None),                       # Youtube ID if exists
"id/vimeo":               ("m", 0, 0, 8, STRING,      None),                       # Vimeo ID if exists
"id/imdb":                ("m", 1, 0, 8, STRING,      None),                       # IMDB ID for movies
"id/guid":                ("m", 0, 0, 8, STRING,      None),                       # Created automatically when asset is created
"id/vod":                 ("m", 0, 0, 8, STRING,      None),                       # VOD KEY
"id/tape":                ("m", 0, 1, 8, STRING,      None),                       # Archive tape ID
"id/umid":                ("m", 0, 1, 8, STRING,      None),

"role/director":          ("m", 1, 0, 7, STRING,      None),
"role/performer":         ("m", 1, 0, 7, STRING,      None),
"role/composer":          ("m", 1, 0, 7, STRING,      None),
"role/cast":              ("m", 1, 0, 7, STRING,      None),                       # Coma delimited cast

#
# Technical (automated extraction)
#
# f - format: created by "meta" service
# q - quality/content: created by "analyzer" service
#
#                               E  I  F

"duration":               ("f", 0, 0, 0, TIMECODE,    None),              # Clip duration. From ffprobe/format/duration. if fails, taken from streams[0]/duration
"start_timecode":         ("f", 0, 0, 0, TIMECODE,    None),
"file/mtime":             ("f", 0, 0, 0, DATETIME,    None),              # Timestamp of file last modification
"file/size":              ("f", 0, 0, 0, INTEGER,     None),              # File size in bytes
"file/format":            ("f", 0, 0, 0, STRING,      None),              # Container format name. from ffprobe/format/format_name
"video/index":            ("f", 0, 0, 0, INTEGER,     None),              # Index of the video track
"video/width":            ("f", 0, 0, 0, INTEGER,     None),              # Video frame / image width (pixels)
"video/height":           ("f", 0, 0, 0, INTEGER,     None),              # Video frame / image height (pixels)
"video/fps":              ("f", 0, 0, 0, FRACTION,    None),
"video/fps_f":            ("f", 0, 0, 0, NUMERIC,     None),
"video/pixel_format":     ("f", 0, 0, 0, STRING,      None),
"video/color_range":      ("f", 0, 0, 0, STRING,      None),
"video/color_space":      ("f", 0, 0, 0, STRING,      None),
"video/aspect_ratio":     ("f", 0, 0, 0, FRACTION,    None),
"video/aspect_ratio_f":   ("f", 0, 0, 0, NUMERIC,     None),
"video/codec":            ("f", 0, 0, 0, STRING,      None),
"video/display_format":   ("f", 1, 1, 0, SELECT,      {"cs" : "urn:ebu:metadata-cs:PictureDisplayFormatCodeCS"}),
"audio/codec":            ("f", 0, 0, 0, STRING,      None),

"qc/state":               ("q", 1, 1, 0, INTEGER,     None),              # Special widget 1 and 2 are reserved for Auto QC failed and passed states
"qc/report":              ("q", 1, 0, 0, TEXT,        None),              # Holds error report from QC Pass and/or rejection/approval message from QC humanoid
"audio/bpm":              ("q", 0, 0, 0, NUMERIC,     None),              # Music BPM
"audio/r128/i":           ("q", 0, 0, 0, NUMERIC,     None),              # Integrated loudness (LUFS)
"audio/r128/t":           ("q", 0, 0, 0, NUMERIC,     None),              # Integrated loudness threshold (LUFS)
"audio/r128/lra":         ("q", 0, 0, 0, NUMERIC,     None),              # LRA (LU)
"audio/r128/lra/t":       ("q", 0, 0, 0, NUMERIC,     None),              # Loudness range threshold (LUFS)
"audio/r128/lra/l":       ("q", 0, 0, 0, NUMERIC,     None),              # LRA Low (LUFS)
"audio/r128/lra/r":       ("q", 0, 0, 0, NUMERIC,     None),              # LRA High (LUFS)
"audio/gain/mean":        ("q", 0, 0, 0, NUMERIC,     None),
"audio/gain/peak":        ("q", 0, 0, 0, NUMERIC,     None),
"audio/silence":          ("q", 0, 0, 0, REGIONS,     None),              # Areas with silent audio
"audio/clipping":         ("q", 0, 0, 0, REGIONS,     None),              # Audio clipping areas
"video/black":            ("q", 0, 0, 0, REGIONS,     None),              # Areas where video is black-only
"video/static":           ("q", 0, 0, 0, REGIONS,     None),              # Areas with static image
"video/is_interlaced":    ("q", 0, 0, 0, BOOLEAN,     None),
}
