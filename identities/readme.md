# Face recognition

This folder is used for facial recognition.

Each sub-folder must be named after the person to recognize, and contain photos of their face.

Example:

- identities/Julien/photo1.png
- identities/Julien/photo2.png
- identities/Noah/photo1.png
- identities/Noah/photo2.png
- ...

Square images work best for accurate face recognition. Make sure the faces are cropped.

When using the face recognition plugin, unknown faces will be assigned a random identity (a UUID), a folder of that name will be created and photos of their faces will be taken and saved in that folder automatically.

Rename those automatically-created folders to the name of the person.