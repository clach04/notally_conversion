# notally_conversion

Conversion tools for [Notally](https://github.com/OmGodse/Notally) notes

## Tools

### Import Text files into Notally

txt2notally_xml.py

Takes in list of (plain) text files to import, generates old style XML file still supported by current releases (e.g. 5.9).
Does the absolute minimum, for example skips create date meta data.

## XML Export/Import format

### Notally 4.8 and earlier

Sample, single note:

    <?xml version='1.0' encoding='UTF-8' standalone='yes' ?>
    <exported-notes>
      <notes>
        <note>
          <color>DEFAULT</color>
          <date-created>1721047246990</date-created>
          <pinned>true</pinned>
          <title>Pinned note title</title>
          <body>Pinned content</body>
        </note>
      </notes>
    </exported-notes>

If date missing, assumes 0, 1970-01-01 00:00:00 gmt0.
If pinned missing, assumes False.


## SQLite3 database

### Notally 5.4 (and earlier, 4.9 https://github.com/OmGodse/Notally/releases/tag/v4.9) schema 2023-08-12

    CREATE TABLE android_metadata (locale TEXT);
    CREATE TABLE `BaseNote` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `type` TEXT NOT NULL, `folder` TEXT NOT NULL, `color` TEXT NOT NULL, `title` TEXT NOT NULL, `pinned` INTEGER NOT NULL, `timestamp` INTEGER NOT NULL, `labels` TEXT NOT NULL, `body` TEXT NOT NULL, `spans` TEXT NOT NULL, `items` TEXT NOT NULL);
    CREATE TABLE `Label` (`value` TEXT NOT NULL, PRIMARY KEY(`value`));
    CREATE TABLE room_master_table (id INTEGER PRIMARY KEY,identity_hash TEXT);


### Notally 5.9 schema 2024-07-14

    CREATE TABLE android_metadata (locale TEXT);
    CREATE TABLE `BaseNote` (`id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, `type` TEXT NOT NULL, `folder` TEXT NOT NULL, `color` TEXT NOT NULL, `title` TEXT NOT NULL, `pinned` INTEGER NOT NULL, `timestamp` INTEGER NOT NULL, `labels` TEXT NOT NULL, `body` TEXT NOT NULL, `spans` TEXT NOT NULL, `items` TEXT NOT NULL, `images` TEXT NOT NULL, `audios` TEXT NOT NULL);
    CREATE TABLE `Label` (`value` TEXT NOT NULL, PRIMARY KEY(`value`));
    CREATE TABLE room_master_table (id INTEGER PRIMARY KEY,identity_hash TEXT);

Sample INSERTs/rows:

    INSERT INTO BaseNote VALUES(1,'LIST','NOTES','DEFAULT','Todo list item created 2024-07-14',0,1721001401029,'[]','','[]','[{"body":"Item 1","checked":false},{"body":"Item 2","checked":false},{"body":"Item 3 - checked","checked":true}]','[]','[]');
    INSERT INTO BaseNote VALUES(2,'NOTE','NOTES','DEFAULT','Note created 2024-07-14',0,1721001443718,'[]','Not content.','[]','[]','[]','[]');
    INSERT INTO BaseNote VALUES(3,'NOTE','NOTES','DEFAULT','Pinned note',1,1721001474199,'[]','Content.','[]','[]','[]','[]');
    INSERT INTO BaseNote VALUES(4,'NOTE','NOTES','DEFAULT','Labelled note',0,1721001487017,'["Label1"]',replace('Content here.\nHas Label1.','\n',char(10)),'[]','[]','[]','[]');
    INSERT INTO BaseNote VALUES(5,'NOTE','NOTES','DEFAULT','Note with image',0,1721001532612,'[]',replace('From file system, ~37Kb 1024x1024  PNG\nStored as webp. TODO check if lossless or lossy.','\n',char(10)),'[]','[]','[{"name":"d9f53103-1b01-4936-b62a-5ef87d54791b.webp","mimeType":"image\/webp"}]','[]');
    INSERT INTO BaseNote VALUES(6,'NOTE','NOTES','DEFAULT','Audio note',0,1721001664568,'[]','Quick voice recording. Stores as m4a. TODO codec details.','[]','[]','[]','[{"name":"fdda1ca6-0b0b-4a1e-a2e6-1203497f465e.m4a","duration":2560,"timestamp":1721001688940}]');
    INSERT INTO BaseNote VALUES(8,'NOTE','DELETED','DEFAULT','Deleted note',0,1721005446277,'[]','This note has been deleted.','[]','[]','[]','[]');
    INSERT INTO BaseNote VALUES(9,'NOTE','ARCHIVED','DEFAULT','Archived note',0,1721005471383,'[]','This note is archived.','[]','[]','[]','[]');
    INSERT INTO BaseNote VALUES(10,'NOTE','NOTES','DEFAULT','Styled note',0,1721005515895,'[]',replace('Plain.\nBold\nItalic\nMono-space\nString-Through\nLink\nhttps://google.com\nNot a link https://google.com\nPlain again.','\n',char(10)),'[{"bold":true,"link":false,"italic":false,"monospace":false,"strikethrough":false,"start":7,"end":11},{"bold":false,"link":false,"italic":true,"monospace":false,"strikethrough":false,"start":12,"end":18},{"bold":false,"link":false,"italic":false,"monospace":true,"strikethrough":false,"start":19,"end":29},{"bold":false,"link":false,"italic":false,"monospace":false,"strikethrough":true,"start":30,"end":44},{"bold":false,"link":true,"italic":false,"monospace":false,"strikethrough":false,"start":45,"end":49},{"bold":false,"link":true,"italic":false,"monospace":false,"strikethrough":false,"start":50,"end":68}]','[]','[]','[]');
    INSERT INTO BaseNote VALUES(11,'NOTE','NOTES','DEFAULT','Note with 2 JPEG images',0,1721005791437,'[]',replace('This was originally a JPEG\n16Kb 720x220\n\n2nd also jpeg, ~29Kb 720x449.','\n',char(10)),'[]','[]','[{"name":"403fafef-d171-4718-a0ec-efddd4d5f67b.jpg","mimeType":"image\/jpeg"},{"name":"5764ebcd-97a2-4d04-a335-ffb76285f4af.jpg","mimeType":"image\/jpeg"}]','[]');

    INSERT INTO Label VALUES('Label1');

int/string types, with json for metadata information (todo lists, labels, attachments).
Difference to previous:

  * new columns; images and audios
  * and in the zip file directories for above
      * Audios - filename appears to be UUID of some kind, file extension/type m4a
      * Images - filename appears to be UUID of some kind, file extension/type webp or jpeg (unclear if webp lossless or lossy)

See schema.json for each release:

 * https://github.com/OmGodse/Notally/blob/master/app/schemas/com.omgodse.notally.room.NotallyDatabase/4.json - 2024-06

Indented DDL for notes table, BaseNote:

    CREATE TABLE `BaseNote` (
        `id` INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        `type` TEXT NOT NULL,  // One of; 
        `folder` TEXT NOT NULL,  // One of; 
        `color` TEXT NOT NULL,  // One of https://github.com/OmGodse/Notally/blob/6c1591e0fee0b0a5717f8fb3b4bdfdd586904e82/app/src/main/java/com/omgodse/notally/room/Color.kt#L3  -- also see Themes, e.g. /app/src/main/res/values/colors.xml
        `title` TEXT NOT NULL,  // May be empty string
        `pinned` INTEGER NOT NULL,  // One of; 0/1 - versus true/false in XML
        `timestamp` INTEGER NOT NULL,  // number of seconds since 1970-01-01 00:00:00 gmt0
        `labels` TEXT NOT NULL,
        `body` TEXT NOT NULL,
        `spans` TEXT NOT NULL,
        `items` TEXT NOT NULL,
        `images` TEXT NOT NULL,
        `audios` TEXT NOT NULL
    );

## Similar/related tools

  * https://github.com/clach04/quillpad_conversion for Quillpad (nee Quillnote), also includes a Notally to Quillpad conversion tool
  * https://github.com/clach04/pysimplenote - for SimpleNote conversion tools
