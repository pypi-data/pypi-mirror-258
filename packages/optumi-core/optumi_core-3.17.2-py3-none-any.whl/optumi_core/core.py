##
## Copyright (C) Optumi Inc - All rights reserved.
##
## You may only use this code under license with Optumi Inc and any distribution or modification is strictly prohibited.
## To receive a copy of the licensing terms please write to contact@optumi.com or visit us at http://www.optumi.com.
##

from .utils import hash_file, split_drive, normalize_path, replace_home_with_tilde
from .sessions import get_session
from .exceptions import OperationCanceled

# Generic Operating System Services
import os, io, datetime, re

# Concurrent execution
from threading import Lock, Thread

# Data Compression and Archiving
import tarfile

# File and Directory Access
import tempfile

# Internet Protocols and Support
import requests
from requests.exceptions import HTTPError
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor

# Internet Data Handling
import json, base64

# Numeric and Mathematical Modules
import math

# Optumi temp dir
TEMP_DIR = tempfile.gettempdir() + "/optumi"

# File transfer constants
CUTOFF_SIZE = 10 * 1024 * 1024  # File transfers beyond 10 MB are chunked
MIN_CHUNK_SIZE = 1 * 1024 * 1024  # 1 MB min file transfer chunk size
MAX_CHUNK_SIZE = 20 * 1024 * 1024  # 20 MB max file transfer chunk size

lock = Lock()

## We need to somehow timeout/remove old progress data from these
compressionProgress = {}
uploadProgress = {}
downloadProgress = {}
launchStatus = {}

appDrive = ""
appHome = ""


def update_path(path):
    global appDrive
    global appHome
    appDrive, appHome = split_drive(path)


update_path("~")
userHome = appHome

def get_app_home():
    return appHome


def get_user_home():
    return userHome


def get_compression_progress(keys):
    data = {}
    try:
        lock.acquire()
        if keys == []:
            for key in compressionProgress:
                data[key] = compressionProgress[key]
        else:
            for key in keys:
                if key in compressionProgress:
                    data[key] = compressionProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data


def get_upload_progress(keys):
    data = {}
    try:
        lock.acquire()
        if keys == []:
            for key in uploadProgress:
                data[key] = uploadProgress[key]
        else:
            for key in keys:
                if key in uploadProgress:
                    data[key] = uploadProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data


def get_download_progress(keys):
    data = {}
    try:
        lock.acquire()
        if keys == []:
            for key in downloadProgress:
                data[key] = downloadProgress[key]
        else:
            for key in keys:
                if key in downloadProgress:
                    data[key] = downloadProgress[key]
    except:
        pass
    finally:
        lock.release()
    return data


def cancel_progress(key):
    data = {}
    try:
        lock.acquire()
        if key in compressionProgress:
            compressionProgress[key]["progress"] = -1
        else:
            compressionProgress[key] = {"progress": -1}
        if key in uploadProgress:
            uploadProgress[key]["progress"] = -1
        else:
            uploadProgress[key] = {"progress": -1}
    except:
        pass
    finally:
        lock.release()
    return data


def get_launch_status(key):
    data = {}
    try:
        lock.acquire()
        data = launchStatus[key]
    except:
        pass
    finally:
        lock.release()
    return data


def get_user_information(includeAll, timestamp=None):
    URL = "/exp/jupyterlab/get-user-information"
    try:
        return get_session().post(
            URL,
            data={
                "includeAll": str(includeAll),
                "timestamp": str(timestamp),
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def set_user_information(param, value):
    URL = "/exp/jupyterlab/set-user-information"
    try:
        return get_session().post(
            URL,
            data={
                "param": param,
                "value": str(value),
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def preview_notebook(profile, programType, includeExisting):
    URL = "/exp/jupyterlab/preview-notebook"

    def get_kwargs():
        return dict(
            data={"includeExisting": str(includeExisting), "programType": programType},
            files=[
                ("profile", ("profile", io.BytesIO(json.dumps(profile).encode("utf-8")))),
            ],
            timeout=120,
        )

    try:
        return get_session().post(URL, get_kwargs=get_kwargs)
    except HTTPError as e:
        return e


def setup_notebook(name, timestamp, notebook, profile, programType):
    URL = "/exp/jupyterlab/setup-notebook"

    def get_kwargs():
        return dict(
            data={
                "name": name,
                "timestamp": timestamp,
                "programType": programType,
            },
            files=[
                (
                    "notebook",
                    (notebook["path"], io.BytesIO(notebook["content"].encode("utf-8"))),
                ),
                (
                    "profile",
                    ("profile", io.BytesIO(json.dumps(profile).encode("utf-8"))),
                ),
            ],
            timeout=120,
        )

    try:
        return get_session().post(URL, get_kwargs=get_kwargs)
    except HTTPError as e:
        return e


def launch_notebook(
    requirementsFile,
    hashes,
    paths,
    creationTimes,
    lastModificationTimes,
    sizes,
    uuid,
    timestamp,
):
    URL = "/exp/jupyterlab/launch-notebook"
    try:
        try:
            lock.acquire()
            if uuid in launchStatus and "status" in launchStatus[uuid] and launchStatus[uuid]["status"] == "Failed":
                raise OperationCanceled("Job canceled")
            launchStatus[uuid] = {"status": "Started"}
        except OperationCanceled:
            raise
        except:
            pass
        finally:
            lock.release()

        def get_kwargs():
            files = [
                ("hashes", ("hashes", io.BytesIO(json.dumps(hashes).encode("utf-8")))),
                ("paths", ("paths", io.BytesIO(json.dumps(paths).encode("utf-8")))),
                (
                    "creationTimes",
                    (
                        "creationTimes",
                        io.BytesIO(json.dumps(creationTimes).encode("utf-8")),
                    ),
                ),
                (
                    "lastModificationTimes",
                    (
                        "lastModificationTimes",
                        io.BytesIO(json.dumps(lastModificationTimes).encode("utf-8")),
                    ),
                ),
                ("sizes", ("sizes", io.BytesIO(json.dumps(sizes).encode("utf-8")))),
            ]

            if requirementsFile != None:
                files.append(
                    (
                        "requirementsFile",
                        ("requirements.txt", io.BytesIO(requirementsFile.encode("utf-8"))),
                    )
                )

            return dict(
                data={
                    "uuid": uuid,
                    "timestamp": timestamp,
                    "jupyterDrive": appDrive,
                    "jupyterHome": appHome,
                    "userHome": userHome,
                },
                files=files,
                timeout=120,
            )

        response = get_session().post(URL, get_kwargs=get_kwargs)

        try:
            lock.acquire()
            if response.status_code == 200:
                launchStatus[uuid] = json.loads(response.text)
                launchStatus[uuid]["status"] = "Finished"
        except:
            pass
        finally:
            lock.release()

    except:
        try:
            lock.acquire()
            launchStatus[uuid]["status"] = "Failed"
        except:
            pass
        finally:
            lock.release()
        raise


# Leave module parameter for compatibility
def stop_notebook(workload, module=None):
    URL = "/exp/jupyterlab/stop-notebook"
    try:
        try:
            lock.acquire()
            launchStatus[workload]["status"] = "Failed"
        except:
            pass
        finally:
            lock.release()

        return get_session().post(
            URL,
            data={
                "workload": workload,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


# Leave module parameter for compatibility
def teardown_notebook(workload, module=None):
    URL = "/exp/jupyterlab/teardown-notebook"
    try:
        try:
            lock.acquire()
            launchStatus[workload]["status"] = "Failed"
        except:
            pass
        finally:
            lock.release()

        return get_session().post(
            URL,
            data={
                "workload": workload,
                "module": module,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def create_callback(key):
    def callback(monitor):
        try:
            lock.acquire()
            uploadProgress[key]["progress"] = monitor.bytes_read
        except:
            pass
        finally:
            lock.release()

    return callback


def upload(session, key, pairs):
    for URL, data, files, path in pairs:

        def get_kwargs():
            fields = []
            for key, value in data.items():
                fields.append((key, value))
            for file in files:
                fields.append(file)

            monitor = MultipartEncoderMonitor(MultipartEncoder(fields=fields), create_callback(key))

            return dict(
                data=monitor,
                headers={"Content-Type": monitor.content_type},
                timeout=14400,  # 4 hour timeout
            )

        try:
            session.post(URL, get_kwargs=get_kwargs)

            if path != None:
                try:
                    os.remove(path)
                except Exception as err:
                    print(err)
        except Exception as err:
            print(err)
    try:
        lock.acquire()
        uploadProgress[key]["progress"] = -1
    except:
        pass
    finally:
        lock.release()


def zip_files(key, inc, files):
    # make the path safe for Linux and windows, while being unique
    path = "." + re.sub(r"\W+", "", key + inc) + ".tgz"
    # put the pack in the temp dir
    path = TEMP_DIR + "/" + path
    files.sort(key=lambda x: os.path.getsize(x))
    # make sure the Optumi temp dir exists
    if not os.path.exists(TEMP_DIR):
        os.makedirs(TEMP_DIR)
    # writing files to a zipfile
    with tarfile.open(path, "w:gz") as tar:
        # writing each file one by one
        for file in files:
            tar.add(file)
            try:
                lock.acquire()
                if compressionProgress[key]["progress"] == -1:
                    raise OperationCanceled("Compression canceled", path)
                compressionProgress[key]["progress"] = compressionProgress[key]["progress"] + 1
            except OperationCanceled:
                raise
            except:
                pass
            finally:
                lock.release()
    return path


def upload_files(key, paths, compress, storageTotal, storageLimit, autoAddOnsEnabled, upload_paths=[]):
    URL = "/exp/jupyterlab/upload-files"
    try:
        if len(paths) != len(upload_paths):
            upload_paths = paths[:]

        zipped_paths = list(zip(paths, upload_paths))
        filesToUpload = []
        ## Check for files in chunks of 1000
        while len(zipped_paths) > 1000:
            chunk = zipped_paths[:1000]
            for exists, file in zip(json.loads(check_if_files_exist(zipped_paths).text)["exists"], chunk):
                if not exists:
                    local_file = file[0]
                    upload_file = file[1]
                    stat = os.stat(local_file)
                    created = datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z"
                    lastModified = datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"
                    filesToUpload.append(
                        (
                            normalize_path(local_file),
                            normalize_path(upload_file, strict=False),
                            os.path.getsize(local_file),
                            created,
                            lastModified,
                        )
                    )
            zipped_paths = zipped_paths[1000:]
        ## Check last chunk
        for exists, file in zip(json.loads(check_if_files_exist(zipped_paths).text)["exists"], zipped_paths):
            if not exists:
                local_file = file[0]
                upload_file = file[1]
                stat = os.stat(local_file)
                created = datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z"
                lastModified = datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z"
                filesToUpload.append(
                    (
                        normalize_path(local_file),
                        normalize_path(upload_file, strict=False),
                        os.path.getsize(local_file),
                        created,
                        lastModified,
                    )
                )

        # Check if the user aborted while we were getting file sizes, setting things up
        try:
            lock.acquire()
            if key in compressionProgress:
                # Handle the case where compression was canceled
                if compressionProgress[key]["progress"] == -1:
                    raise OperationCanceled("Compression canceled")
        except OperationCanceled as e:
            raise e
        except Exception as e:
            pass
        finally:
            lock.release()

        if len(filesToUpload) > 0:
            # Check if the user has enough space left in his storage account to upload the file
            uploadTotal = sum([x[2] for x in filesToUpload])

            if (not autoAddOnsEnabled) and (uploadTotal + storageTotal > storageLimit):
                try:
                    lock.acquire()
                    # See FileTracker.ts for error values (look at UploadStatus)
                    compressionProgress[key] = {"progress": -2}
                    uploadProgress[key] = {"progress": -1}
                except Exception as e:
                    pass
                finally:
                    lock.release()
                # We want to bail out of this upload
                return

            # Sort by file size
            filesToUpload.sort(key=lambda x: x[2], reverse=True)

            if compress:
                try:
                    lock.acquire()
                    compressionProgress[key] = {
                        "progress": 0,
                        "total": len(filesToUpload),
                    }
                except Exception as e:
                    pass
                finally:
                    lock.release()

            MAX_SIZE = 5 * 1024 * 1024 * 1024

            fileChunks = [[]]
            metadataChunks = [{}]
            totalSize = 0
            for local_file, upload_file, size, created, lastModified in filesToUpload:
                # Check if the user aborted before we process and potentially compress a new file
                try:
                    lock.acquire()
                    if key in compressionProgress:
                        # Handle the case where compression was canceled
                        if compressionProgress[key]["progress"] == -1:
                            raise OperationCanceled("Compression canceled")
                except OperationCanceled as e:
                    raise e
                except Exception as e:
                    pass
                finally:
                    lock.release()

                if size > MAX_SIZE:
                    print("Skipping upload of files " + str(paths) + ", file " + local_file + " exceeds " + str(MAX_SIZE) + " limit")
                    try:
                        lock.acquire()
                        # See FileTracker.ts for error values (look at UploadStatus)
                        compressionProgress[key] = {"progress": -3}
                        uploadProgress[key] = {"progress": -1}
                    except Exception as e:
                        pass
                    finally:
                        lock.release()
                    # We want to bail out of this upload
                    return
                elif totalSize + size > MAX_SIZE:
                    # If the next file takes us over 5GB, this is the end of the chunk
                    if compress:
                        zipFile = zip_files(key, str(len(fileChunks)), fileChunks[-1])
                        fileChunks[-1] = [zipFile]

                    # Reset variables for the next chunk of files
                    fileChunks.append([])
                    metadataChunks.append({})
                    totalSize = 0
                else:
                    fileChunks[-1].append(local_file)
                    metadataChunks[-1][split_drive(local_file)[1]] = {
                        "path": replace_home_with_tilde(local_file),
                        "upload_path": replace_home_with_tilde(upload_file, strict=False),
                        "created": created,
                        "lastModified": lastModified,
                    }
                    totalSize += size

            # Compress the last chunk if necessary
            if compress:
                zipFile = zip_files(key, str(len(fileChunks)), fileChunks[-1])
                fileChunks[-1] = [zipFile]

            # We need to add up the total upload size before we start uploading
            totalSize = 0
            for chunk in fileChunks:
                for file in chunk:
                    totalSize += os.path.getsize(file)
            try:
                lock.acquire()
                if key in compressionProgress:
                    # Handle the case where compression was canceled
                    if compressionProgress[key]["progress"] == -1:
                        raise OperationCanceled("Compression canceled")
                    compressionProgress[key]["progress"] = -1
                uploadProgress[key] = {"progress": 0, "total": totalSize}
            except OperationCanceled as e:
                raise e
            except Exception as e:
                pass
            finally:
                lock.release()

            requests = []
            for chunk, metadata in zip(fileChunks, metadataChunks):
                files = []
                for file in chunk:
                    files.append(("files", (file, open(file, "rb"))))

                files.append(
                    (
                        "metadata",
                        ("metadata", io.BytesIO(json.dumps(metadata).encode("utf-8"))),
                    )
                )

                data = {
                    "compressed": str(compress),
                }

                if compress:
                    requests.append((URL, data, files, chunk[0]))
                else:
                    requests.append((URL, data, files, None))

                # This thread will set the upload state to none when it is finished
                Thread(
                    target=upload,
                    args=(
                        get_session(),
                        key,
                        requests,
                    ),
                ).start()
        else:
            # We want to record the no files need to be uploaded, otherwise the extension will keep asking
            try:
                lock.acquire()
                if compress:
                    compressionProgress[key] = {"progress": -1, "total": 0}
                uploadProgress[key] = {"progress": -1, "total": 0}
            except Exception as e:
                pass
            finally:
                lock.release()
    except OperationCanceled as e:
        cleanup_progress(key, compress)
        if e.pathToRemove and os.path.exists(e.pathToRemove):
            os.remove(e.pathToRemove)
        return e
    except HTTPError as e:
        cleanup_progress(key, compress)
        return e


def cleanup_progress(key, compress):
    # Clean up ongoing progress in the case of a failure
    if key:
        try:
            lock.acquire()
            if compress:
                # Cancel compression progress
                if key in compressionProgress:
                    compressionProgress[key] = {"progress": -1, "total": 0}
            # Cancel upload progress
            if key in uploadProgress:
                uploadProgress[key] = {"progress": -1, "total": 0}
        except Exception:
            pass
        finally:
            lock.release()


def check_if_files_exist(zipped_paths):
    URL = "/exp/jupyterlab/check-if-files-exist"
    try:
        stats = [os.stat(f[0]) if os.path.isfile(f[0]) else None for f in zipped_paths]
        creationTimes = [datetime.datetime.utcfromtimestamp(stat.st_ctime).isoformat() + "Z" if stat != None else None for stat in stats]
        lastModificationTimes = [datetime.datetime.utcfromtimestamp(stat.st_mtime).isoformat() + "Z" if stat != None else None for stat in stats]

        return get_session().post(
            URL,
            data={
                "autoAdd": str(True),
            },
            files=[
                (
                    "paths",
                    (
                        "paths",
                        io.BytesIO(json.dumps([replace_home_with_tilde(file[1], strict=False) for file in zipped_paths]).encode("utf-8")),
                    ),
                ),
                (
                    "hashes",
                    (
                        "hashes",
                        io.BytesIO(json.dumps([hash_file(f[0]) for f in zipped_paths]).encode("utf-8")),
                    ),
                ),
                (
                    "sizes",
                    (
                        "sizes",
                        io.BytesIO(json.dumps([str(os.path.getsize(f[0])) for f in zipped_paths]).encode("utf-8")),
                    ),
                ),
                (
                    "creationTimes",
                    (
                        "creationTimes",
                        io.BytesIO(json.dumps(creationTimes).encode("utf-8")),
                    ),
                ),
                (
                    "lastModificationTimes",
                    (
                        "lastModificationTimes",
                        io.BytesIO(json.dumps(lastModificationTimes).encode("utf-8")),
                    ),
                ),
            ],
            timeout=120,
        )
    except HTTPError as e:
        return e


def get_machines():
    URL = "/exp/jupyterlab/get-machines"
    try:
        return get_session().get(URL, timeout=120)
    except HTTPError as e:
        return e


def get_workloads():
    URL = "/exp/jupyterlab/get-workloads"
    try:
        return get_session().get(URL, timeout=120)
    except HTTPError as e:
        return e


def get_workload_properties(workload, workloadProperties, moduleProperties):
    URL = "/exp/jupyterlab/get-workload-properties"
    try:
        return get_session().post(
            URL,
            data={
                "workload": workload,
                "workloadProperties": workloadProperties,
                "moduleProperties": moduleProperties,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def pull_workload_config(workload):
    URL = "/exp/jupyterlab/pull-workload-config"
    try:
        return get_session().post(
            URL,
            data={
                "workload": workload,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def push_workload_config(workload, profile):
    URL = "/exp/jupyterlab/push-workload-config"
    try:
        return get_session().post(
            URL,
            data={
                "workload": workload,
                "profile": profile,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def get_profile(profileName):
    URL = "/exp/jupyterlab/get-profile"
    try:
        return get_session().post(
            URL,
            data={
                "profileName": profileName,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def delete_profile(profileName):
    URL = "/exp/jupyterlab/delete-profile"
    try:
        return get_session().post(
            URL,
            data={
                "profileName": profileName,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def create_profile(profileName, profile, associated_base_names):
    URL = "/exp/jupyterlab/create-profile"
    try:
        return get_session().post(
            URL,
            data={
                "profileName": profileName,
                "profile": json.dumps(profile),
                "associatedBaseNames": associated_base_names,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def update_profile(profileName, profile, associated_base_names):
    URL = "/exp/jupyterlab/update-profile"
    try:
        return get_session().post(
            URL,
            data={
                "profileName": profileName,
                "profile": json.dumps(profile),
                "associatedBaseNames": associated_base_names,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def get_profiles():
    URL = "/exp/jupyterlab/get-profiles"
    try:
        return get_session().get(
            URL,
            timeout=120,
        )
    except HTTPError as e:
        return e


def pull_package_update(nbKeys):
    URL = "/exp/jupyterlab/pull-package-update"
    try:
        # We need to send something in the body of this message otherwise the POST will fail
        if len(nbKeys) == 0:
            data = {"empty": str(True)}
        else:
            data = {nbKeys: nbKeys}

        return get_session().post(URL, data=data, timeout=120)
    except HTTPError as e:
        return e


def push_package_update(nbKey, label, hashes, paths, update):
    URL = "/exp/jupyterlab/push-package-update"
    try:
        data = {
            "nbKey": nbKey,
        }
        if label != None:
            data["label"] = label
        files = [("update", ("update", io.BytesIO(update.encode("utf-8"))))]
        if paths != None:
            files.append(("hashes", ("hashes", io.BytesIO(",".join(hashes).encode("utf-8"))))),
            files.append(("paths", ("paths", io.BytesIO(",".join(paths).encode("utf-8"))))),

        return get_session().post(URL, data=data, files=files, timeout=120)
    except HTTPError as e:
        return e


def get_integrations():
    URL = "/exp/jupyterlab/get-integrations"
    try:
        return get_session().get(URL, timeout=120)
    except HTTPError as e:
        return e


def add_integration(name, info, overwrite):
    URL = "/exp/jupyterlab/add-integration"
    try:
        return get_session().post(
            URL,
            data={
                "name": name,
                "info": info,
                "overwrite": overwrite,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def rename_integration(oldName, newName):
    URL = "/exp/jupyterlab/rename-integration"
    try:
        return get_session().post(
            URL,
            data={
                "oldName": oldName,
                "newName": newName,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def remove_integration(name):
    URL = "/exp/jupyterlab/remove-integration"
    try:
        return get_session().post(
            URL,
            data={
                "name": name,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def push_workload_initializing_update(uuid, update):
    URL = "/exp/jupyterlab/push-workload-initializing-update"
    try:
        return get_session().post(
            URL,
            data={
                "uuid": uuid,
                "update": update,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def pull_workload_status_updates(uuids, lastInitializingLines, lastPreparingLines, lastRunningLines):
    URL = "/exp/jupyterlab/pull-workload-status-updates"
    try:
        return get_session().post(
            URL,
            data={
                "uuids": uuids,
                "lastInitializingLines": lastInitializingLines,
                "lastPreparingLines": lastPreparingLines,
                "lastRunningLines": lastRunningLines,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def pull_module_status_updates(
    workloadUUIDs,
    moduleUUIDs,
    lastUpdateLines,
    lastOutputLines,
    lastMonitorings,
    lastPatches,
    includeAll,
):
    URL = "/exp/jupyterlab/pull-module-status-updates"
    try:
        data = {
            "workloadUUIDs": workloadUUIDs,
            "moduleUUIDs": moduleUUIDs,
            "lastUpdateLines": lastUpdateLines,
            "lastOutputLines": lastOutputLines,
            "lastMonitorings": lastMonitorings,
            "lastPatches": lastPatches,
            "includeAll": includeAll,
        }

        return get_session().post(URL, data=data, timeout=120)
    except HTTPError as e:
        return e


def list_files():
    URL = "/exp/jupyterlab/list-files"
    try:
        return get_session().get(URL, timeout=120)
    except HTTPError as e:
        return e


def delete_files(hashes, paths, creationTimes, directory):
    URL = "/exp/jupyterlab/delete-files"
    try:
        return get_session().post(
            URL,
            data={
                "directory": directory,
            },
            files=[
                ("hashes", ("hashes", io.BytesIO(json.dumps(hashes).encode("utf-8")))),
                ("paths", ("paths", io.BytesIO(json.dumps(paths).encode("utf-8")))),
                (
                    "creationTimes",
                    (
                        "creationTimes",
                        io.BytesIO(json.dumps(creationTimes).encode("utf-8")),
                    ),
                ),
            ],
            timeout=120,
        )
    except HTTPError as e:
        return e


def save_file(fileName, content, overwrite):
    file = os.path.expanduser(fileName)
    if not overwrite:
        newName = file
        num = 1
        while os.path.exists(newName) and os.path.isfile(newName):
            f, ext = os.path.splitext(file)
            newName = f + "(" + str(num) + ")" + ext
            num += 1
        file = newName
    dirs = os.path.dirname(file)
    if dirs != "":
        os.makedirs(dirs, exist_ok=True)
    with open(file, "wb") as f:
        f.write(base64.decodebytes(content.getvalue()))


def add_content(content, decoded):
    # Remove starting or ending " so we can look at only , when splitting the string
    if decoded != "" and decoded[0] == '"':
        decoded = decoded[1:]
    if decoded != "" and decoded[-1] == '"':
        decoded = decoded[:-1]
    encoded = decoded.encode("ascii")
    content.write(encoded)


def download_files_helper(URL, formHashes, savePaths, overwrite):
    def get_kwargs():
        return dict(
            files=[
                ("hashes", ("hashes", io.BytesIO(json.dumps(formHashes).encode("utf-8")))),
            ],
            timeout=120,
        )

    response = get_session().post(URL, get_kwargs=get_kwargs)

    blocksize = 4096

    content = io.BytesIO()
    for read in response.iter_content(chunk_size=blocksize):
        decoded = read.decode("ascii")
        if decoded != "" and decoded[0] == "[":
            # Remove the opening ["
            decoded = decoded[1:]
        if decoded != "" and decoded[-1] == "]":
            # Remove the ending "]"
            decoded = decoded[:-1]
        if "," in decoded:
            split = decoded.split(",")
            for chunk in split[:-1]:
                add_content(content, chunk)
                save_file(savePaths.pop(0), content, overwrite)
                content = io.BytesIO()
            # Handle the last chunk like the else case below
            add_content(content, split[-1])
        else:
            add_content(content, decoded)

    # Save the last file
    save_file(savePaths.pop(0), content, overwrite)


def download_file_chunk_helper(hash, fileName, savePath, size, overwrite):
    URL = "/exp/jupyterlab/download-file-chunk"

    # Start with chunk thats 1 percent of the total size
    CHUNK_SIZE = size // 100
    # Round to the nearest megabyte for cleanliness
    CHUNK_SIZE = math.ceil(CHUNK_SIZE / (1024 * 1024)) * (1024 * 1024)
    # Apply min and max
    if CHUNK_SIZE < MIN_CHUNK_SIZE:
        CHUNK_SIZE = MIN_CHUNK_SIZE
    if CHUNK_SIZE > MAX_CHUNK_SIZE:
        CHUNK_SIZE = MAX_CHUNK_SIZE

    # Set up file
    file = normalize_path(savePath, strict=False)
    if not overwrite:
        newName = file
        num = 1
        while os.path.exists(newName) and os.path.isfile(newName):
            f, ext = os.path.splitext(file)
            newName = f + "(" + str(num) + ")" + ext
            num += 1
        file = newName
    dirs = os.path.dirname(file)
    if dirs != "":
        os.makedirs(dirs, exist_ok=True)
    f = open(file, "wb")

    offset = 0

    while True:
        response = get_session().post(
            URL,
            data={
                "hash": hash,
                "offset": str(offset),
                "chunkSize": str(CHUNK_SIZE),
            },
            timeout=120,
        )
        chunk = response.content

        offset += len(chunk)

        if not chunk:
            break

        f.write(chunk)

    f.close()


def download_files(key, hashes, paths, sizes, overwrite, directory):
    URL = "/exp/jupyterlab/download-files"

    try:
        total = sum(sizes)
        try:
            lock.acquire()
            downloadProgress[key] = {"progress": 0, "total": total}
        except:
            pass
        finally:
            lock.release()

        savePaths = paths

        if directory != None:
            dirs = normalize_path(directory, strict=False)
            if not overwrite:
                newName = dirs
                num = 0
                while os.path.exists(newName) and os.path.isdir(newName):
                    num += 1
                    newName = dirs + "(" + str(num) + ")"
            if num > 0:
                savePaths = [path.replace(directory, directory + "(" + str(num) + ")", 1) for path in savePaths]

        filesToDownload = zip(hashes, paths, savePaths, sizes)
        # Sort by file size
        filesToDownload = sorted(filesToDownload, key=lambda x: x[3])

        # These files will be aggregated in a group with a max size of CUTOFF_SIZE, and downloaded as a group
        groupFiles = [x for x in filesToDownload if x[3] < CUTOFF_SIZE]
        # These files will be download individually in chunks of CHUNK_SIZE
        chunkFiles = [x for x in filesToDownload if x[3] >= CUTOFF_SIZE]

        # download group files
        totalSize = 0
        formHashes = []
        fileNames = []
        saveNames = []
        for hash, file, savePath, size in groupFiles:
            if totalSize + size > CUTOFF_SIZE:
                download_files_helper(URL, formHashes, saveNames, overwrite)

                # Reset variables for the next chunk of files
                totalSize = 0
                formHashes = []
                fileNames = []
                saveNames = []
            totalSize += size
            formHashes.append(hash)
            fileNames.append(file)
            saveNames.append(savePath)

        if len(saveNames) > 0:
            # Download the remaining files
            download_files_helper(URL, formHashes, saveNames, overwrite)

        for hash, file, savePath, size in chunkFiles:
            download_file_chunk_helper(hash, file, savePath, size, overwrite)

        # Make sure we mark the download as completed
        try:
            lock.acquire()
            downloadProgress[key] = {"progress": -1, "total": total}
        except:
            pass
        finally:
            lock.release()

        return
    except HTTPError as e:
        return e


def get_notebook_output_files(workloadUUID, moduleUUID, key, paths, sizes, overwrite, directory):
    URL = "/exp/jupyterlab/get-notebook-output-file"

    def get_kwargs():
        return dict(
            data={
                "workloadUUID": workloadUUID,
                "moduleUUID": moduleUUID,
            },
            files=[
                (
                    "paths",
                    (
                        "paths",
                        io.BytesIO(json.dumps([replace_home_with_tilde(path) for path in paths]).encode("utf-8")),
                    ),
                ),
            ],
            timeout=600,
        )

    try:
        # Tell the controller to put the files in blob storage early, this will return the hashes, which we need to download the files
        response = get_session().post(URL, get_kwargs=get_kwargs)
        hashes = json.loads(response.content)

        # Download the files
        return download_files(key, hashes, paths, sizes, overwrite, directory)
    except HTTPError as e:
        return e


def get_balance(startTime, endTime):
    URL = "/exp/jupyterlab/get-balance"
    try:
        return get_session().post(
            URL,
            data={
                "startTime": startTime,
                "endTime": endTime,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def get_detailed_billing(startTime, endTime):
    URL = "/exp/jupyterlab/get-detailed-billing"
    try:
        return get_session().post(
            URL,
            data={
                "startTime": startTime,
                "endTime": endTime,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def delete_machine(uuid):
    URL = "/exp/jupyterlab/release-machine"
    try:
        return get_session().post(
            URL,
            data={
                "uuid": uuid,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def change_password(loginName, oldPassword, newPassword):
    URL = "/exp/jupyterlab/change-password"
    try:
        return get_session().post(
            URL,
            data={
                "loginName": loginName,
                "oldPassword": oldPassword,
                "newPassword": newPassword,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def create_portal(redirect):
    URL = "/exp/jupyterlab/create-portal"
    try:
        return get_session().post(
            URL,
            data={
                "redirect": redirect,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def create_checkout(items, redirect):
    URL = "/exp/jupyterlab/create-checkout"
    try:
        return get_session().post(
            URL,
            data={
                "items": items,
                "redirect": redirect,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def cancel_subscription():
    URL = "/exp/jupyterlab/cancel-subscription"
    try:
        return get_session().get(URL, timeout=120)
    except HTTPError as e:
        return e


def get_connection_token(forceNew):
    URL = "/exp/jupyterlab/get-connection-token"
    try:
        return get_session().post(
            URL,
            data={
                "forceNew": forceNew,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def redeem_signup_code(signupCode):
    URL = "/exp/jupyterlab/redeem-signup-code"
    try:
        return get_session().post(
            URL,
            data={
                "signupCode": signupCode,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def send_notification(message):
    URL = "/exp/jupyterlab/send-notification"
    try:
        return get_session().post(
            URL,
            data={
                "message": message,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def send_verification_code(phoneNumber):
    URL = "/exp/jupyterlab/send-verification-code"
    try:
        return get_session().post(
            URL,
            data={
                "phoneNumber": phoneNumber,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def check_verification_code(phoneNumber, code):
    URL = "/exp/jupyterlab/check-verification-code"
    try:
        return get_session().post(
            URL,
            data={
                "phoneNumber": phoneNumber,
                "code": code,
            },
            timeout=120,
        )
    except HTTPError as e:
        return e


def clear_phone_number():
    URL = "/exp/jupyterlab/clear-phone-number"
    try:
        return get_session().get(
            URL,
            timeout=120,
        )
    except HTTPError as e:
        return e
