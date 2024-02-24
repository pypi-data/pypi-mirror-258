import torch

def batch_affine_transform(A, B):
    """
    Finds transform corresponding from A -> B
    """
    assert A.shape == B.shape

    # find mean column wise
    centroid_A = torch.mean(A, axis=-1)[...,None] # (3)
    centroid_B = torch.mean(B, axis=-1)[...,None] # (3)

    H = (A - centroid_A) @ (B - centroid_B).mT

    # find rotation
    U, S, Vt = torch.linalg.svd(H)
    R = Vt.mT @ U.mT
    U[R.det() < 0,...,1] *= -1 # fix flip
    R = Vt.mT @ U.mT

    t = -R @ centroid_A + centroid_B

    return R, t


def face_verts_arap_loss(stable_face_verts, face_verts, rigidity_weights=1):
    Rs, ts = batch_affine_transform(stable_face_verts, face_verts)
    rigid_face_verts = (Rs @ stable_face_verts + ts).detach()

    return torch.mean(rigidity_weights * ((face_verts - rigid_face_verts) ** 2))
