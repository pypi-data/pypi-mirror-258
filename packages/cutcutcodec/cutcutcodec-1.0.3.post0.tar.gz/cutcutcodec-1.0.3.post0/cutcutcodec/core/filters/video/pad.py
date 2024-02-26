#!/usr/bin/env python3

"""Resizes an image while keeping the proportions."""

import numbers
import typing

import numpy as np

from cutcutcodec.core.classes.frame_video import FrameVideo


def pad_keep_ratio(
    frame: typing.Union[np.ndarray, FrameVideo],
    shape: typing.Union[tuple[numbers.Integral, numbers.Integral], list[numbers.Integral]],
) -> typing.Union[np.ndarray, FrameVideo]:
    """Pad the frame with transparent borders.

    Parameters
    ----------
    frame : np.ndarray or cutcutcodec.core.classes.frame_video.FrameVideo
        The image to be padded. If a numpy array is provide, the format
        has to match with the video frame specifications.
    shape : int and int
        The pixel dimensions of the returned frame.
        Each dimension has to be larger or equal to the provided frame.
        The convention adopted is the numpy convention (height, width).

    Returns
    -------
    np.ndarray or cutcutcodec.core.classes.frame_video.FrameVideo
        The padded frame homogeneous with the input.
        The underground datas are not sharded with the input. A safe copy is done.

    Examples
    --------
    >>> import torch
    >>> from cutcutcodec.core.classes.frame_video import FrameVideo
    >>> from cutcutcodec.core.filters.video.pad import pad_keep_ratio
    >>> ref = FrameVideo(0, torch.full((4, 8, 3), 128, dtype=torch.uint8))
    >>> pad_keep_ratio(ref, (8, 8))[..., 3]  # alpha layer
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255],
            [255, 255, 255, 255, 255, 255, 255, 255],
            [  0,   0,   0,   0,   0,   0,   0,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>> pad_keep_ratio(ref, (4, 9)).convert(1)[..., 0]  # as gray
    tensor([[128, 128, 128, 128, 128, 128, 128, 128,   0],
            [128, 128, 128, 128, 128, 128, 128, 128,   0],
            [128, 128, 128, 128, 128, 128, 128, 128,   0],
            [128, 128, 128, 128, 128, 128, 128, 128,   0]], dtype=torch.uint8)
    >>> pad_keep_ratio(ref, (6, 10)).convert(1)[..., 0]  # as gray
    tensor([[  0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
            [  0, 128, 128, 128, 128, 128, 128, 128, 128,   0],
            [  0, 128, 128, 128, 128, 128, 128, 128, 128,   0],
            [  0, 128, 128, 128, 128, 128, 128, 128, 128,   0],
            [  0, 128, 128, 128, 128, 128, 128, 128, 128,   0],
            [  0,   0,   0,   0,   0,   0,   0,   0,   0,   0]], dtype=torch.uint8)
    >>>
    """
    # case FrameVideo
    if isinstance(frame, FrameVideo):
        return FrameVideo(frame.time, pad_keep_ratio(frame.numpy(force=True), shape))

    # verif case np.ndarray
    assert isinstance(frame, np.ndarray), frame.__class__.__name__
    assert frame.ndim == 3, frame.shape
    assert frame.shape[0] >= 1, frame.shape
    assert frame.shape[1] >= 1, frame.shape
    assert frame.shape[2] in {1, 2, 3, 4}, frame.shape
    assert frame.dtype == np.uint8, frame.dtype
    assert len(shape) == 2, len(shape)
    assert all(isinstance(s, numbers.Integral) and s >= 1 for s in shape), shape
    assert shape >= frame.shape[:1], f"no crop from {frame.shape} to {shape}, only padding"

    # optimization, avoid management of alpha channel
    if frame.shape[:2] == shape:
        return frame.copy()

    # manage alpha channel
    channels = {1: 2, 2: 2, 3: 4, 4: 4}[frame.shape[2]]
    frame_paded = np.empty((*shape, channels), dtype=np.uint8)  # 1500 faster than np.zeros
    if (dec_h := shape[0]-frame.shape[0]):  # if height needs padding
        dec_h //= 2
        frame_paded[:dec_h, :, -1] = 0  # set band transparent
        frame_paded[frame.shape[0]+dec_h:, :, -1] = 0
    if (dec_w := shape[1]-frame.shape[1]):  # if width needs padding
        dec_w //= 2
        frame_paded[dec_h:frame.shape[0]+dec_h, :dec_w, -1] = 0  # set band transparent
        frame_paded[dec_h:frame.shape[0]+dec_h, frame.shape[1]+dec_w, -1] = 0
    if frame.shape[2] != channels:  # if no alpha specify
        frame_paded[dec_h:frame.shape[0]+dec_h, dec_w:frame.shape[1]+dec_w] = 255  # blind

    # copy data
    frame_paded[dec_h:frame.shape[0]+dec_h, dec_w:frame.shape[1]+dec_w, :frame.shape[2]] = frame
    return frame_paded
