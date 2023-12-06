from typing import List, Type
import numpy as np
import omni.ext
import omni.ui as ui
import omni.usd
import time
import asyncio
from scipy.spatial.transform import Rotation as R
import os

def parse_csv(csv_path):
    return np.loadtxt(csv_path, delimiter=',')

def clack_clack():
    print("clack_clack")
    import omni.replicator.core as rep
    from pxr import Gf, UsdGeom, Usd, Sdf
    from omni.kit.viewport.utility import get_active_viewport

    with rep.new_layer(name="layer_1"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        usd = os.path.join(script_dir, "resources/usd/clack/clack_2.usd")

        stage = Usd.Stage.Open(usd)

        curr_stage = omni.usd.get_context().get_stage()
        if curr_stage.GetPrimAtPath("/Replicator"):
            delete_prim("/Replicator")
        else:

            # if stage.GetPrimAtPath("/Replicator/Ref_Xform"):
            #     rig_path = f'/Replicator/Ref_Xfrom/Ref/rig_clack'
            # else:
            #     rig_path = f'/Replicator/Ref_Xfrom_01/Ref/rig_clack'
            rig_path = f'/Replicator/Ref_Xform/Ref/rig_clack'

            lever_path = "/Replicator/Ref_Xform/Ref/rig_clack/arm_clack/ub_root/ub_bot/ub_top"
            lever_prim = stage.GetPrimAtPath(lever_path)
            lever_xform = UsdGeom.Xformable(lever_prim)
            if lever_xform:
                rotate_op = lever_xform.AddRotateXYZOp(UsdGeom.XformOp.PrecisionDouble, UsdGeom.XformOp.TransformSpace.Local)

            
            rep.create.from_usd(usd)
            # rig = rep.get.prim_at_path(rig_path)

            csv = os.path.join(script_dir, "resources/data/RotLoc.csv")
            sequence = parse_csv(csv)
            
            translations = 200 * sequence[:,:3]
            trans_list = translations.tolist()
            r = R.from_quat(sequence[:,3:][:, [1, 2, 3, 0]])
            euler_angles = r.as_euler('zyx', degrees=True)
            euler_list = euler_angles.tolist()

            rig = rep.get.prim_at_path('/Replicator/Ref_Xform/Ref/rig_clack')

            # # astronaut_scene= rep.create.from_usd(usd, semantics=[('class', 'astronaut_scene')])
            viewport = get_active_viewport()
            camera_path = "/Replicator/Ref_Xform/Ref/Camera/Camera"
            viewport.camera_path = camera_path
            camera = viewport.get_active_camera()
            
            render_product = rep.create.render_product(camera_path, (1024, 1024))
            render_product2 = rep.create.render_product(camera_path, (512, 512))
            writer = rep.WriterRegistry.get("BasicWriter")
            writer.initialize(output_dir="/home/manifold6/Downloads/test_data/test1", rgb=True, bounding_box_2d_tight=True)
            writer.attach([render_product, render_product2])

            frames = 2*len(sequence)

            # lever_sub_path = "/arm_clack/ub_root/ub_bot/ub_top"

            # # Get current location and rotation
            # lever_prim = stage.GetPrimAtPath(
            #     "/Replicator/Ref_Xform/Ref/rig_clack/arm_clack/ub_root/ub_bot/ub_top" # "/root/rig_clack" + lever_sub_path
            # )


            lever_rep = rep.get.prim_at_path(
                "/Replicator/Ref_Xform/Ref/rig_clack/arm_clack/ub_root/ub_bot/ub_top"
            ) #rig_path + lever_sub_path)
            
            # lever_local_transform = omni.usd.get_local_transform_SRT(lever_prim)
            # scale = lever_local_transform[0]
            # rotation = lever_local_transform[1]
            # location = lever_local_transform[2]
            with rep.trigger.on_frame(num_frames=frames):
                with rig:                                
                    rep.modify.pose(
                        # position=rep.distribution.sequence(trans_list),
                        # rotation=rep.distribution.sequence(euler_list)
                        position=rep.distribution.uniform((-80,-80,-30),(80,80,30)),
                        rotation=rep.distribution.uniform((0,0,0),(360,360,360))
                    )
            
            # with rep.trigger.on_frame(num_frames=frames):
            #     with lever_rep:
            #         rep.modify.pose(
            #             rotation=rep.distribution.uniform((0,0,0),(0,360,0))
            #         )
            #     # pass
            rep.orchestrator.run()

            # return []


def render_scene(entities, implants, render_views, render_settings):
        """
        Description:
        Render a scene with the given entities and implants.
        Args:
        entities (list): List of entities to render.
        """
        import omni.replicator.core as rep
        from pxr import Gf, UsdGeom, Usd, Sdf
        from omni.kit.viewport.utility import get_active_viewport

        with rep.new_layer(name="layer_1"):
            usd = '/home/manifold6/Documents/clack/clack_2.usd'

            stage = Usd.Stage.Open(usd)

            curr_stage = omni.usd.get_context().get_stage()
            if curr_stage.GetPrimAtPath("/Replicator"):
                delete_prim("/Replicator")
            else:

                # if stage.GetPrimAtPath("/Replicator/Ref_Xform"):
                #     rig_path = f'/Replicator/Ref_Xfrom/Ref/rig_clack'
                # else:
                #     rig_path = f'/Replicator/Ref_Xfrom_01/Ref/rig_clack'
                rig_path = f'/Replicator/Ref_Xform/Ref/rig_clack'

                lever_path = "/Replicator/Ref_Xform/Ref/rig_clack/arm_clack/ub_root/ub_bot/ub_top"
                lever_prim = stage.GetPrimAtPath(lever_path)
                lever_xform = UsdGeom.Xformable(lever_prim)
                if lever_xform:
                    rotate_op = lever_xform.AddRotateXYZOp(UsdGeom.XformOp.PrecisionDouble, UsdGeom.XformOp.TransformSpace.Local)

                
                rep.create.from_usd(usd)
                # rig = rep.get.prim_at_path(rig_path)

                csv = "/home/manifold6/Documents/RotLoc.csv"
                sequence = parse_csv(csv)
                
                translations = 200 * sequence[:,:3]
                trans_list = translations.tolist()
                r = R.from_quat(sequence[:,3:][:, [1, 2, 3, 0]])
                euler_angles = r.as_euler('zyx', degrees=True)
                euler_list = euler_angles.tolist()

                rig = rep.get.prim_at_path('/Replicator/Ref_Xform/Ref/rig_clack')

                # # astronaut_scene= rep.create.from_usd(usd, semantics=[('class', 'astronaut_scene')])
                viewport = get_active_viewport()
                camera_path = "/Replicator/Ref_Xform/Ref/Camera/Camera"
                viewport.camera_path = camera_path
                camera = viewport.get_active_camera()
                
                render_product = rep.create.render_product(camera_path, (1024, 1024))
                render_product2 = rep.create.render_product(camera_path, (512, 512))
                writer = rep.WriterRegistry.get("BasicWriter")
                writer.initialize(output_dir="/home/manifold6/Downloads/test_data/test1", rgb=True, bounding_box_2d_tight=True)
                writer.attach([render_product, render_product2])

                frames = 2*len(sequence)

                # lever_sub_path = "/arm_clack/ub_root/ub_bot/ub_top"

                # # Get current location and rotation
                # lever_prim = stage.GetPrimAtPath(
                #     "/Replicator/Ref_Xform/Ref/rig_clack/arm_clack/ub_root/ub_bot/ub_top" # "/root/rig_clack" + lever_sub_path
                # )


                lever_rep = rep.get.prim_at_path(
                    "/Replicator/Ref_Xform/Ref/rig_clack/arm_clack/ub_root/ub_bot/ub_top"
                ) #rig_path + lever_sub_path)
                
                # lever_local_transform = omni.usd.get_local_transform_SRT(lever_prim)
                # scale = lever_local_transform[0]
                # rotation = lever_local_transform[1]
                # location = lever_local_transform[2]
                with rep.trigger.on_frame(num_frames=frames):
                    with rig:                                
                        rep.modify.pose(
                            # position=rep.distribution.sequence(trans_list),
                            # rotation=rep.distribution.sequence(euler_list)
                            position=rep.distribution.uniform((-80,-80,-30),(80,80,30)),
                            rotation=rep.distribution.uniform((0,0,0),(360,360,360))
                        )
                
                # with rep.trigger.on_frame(num_frames=frames):
                #     with lever_rep:
                #         rep.modify.pose(
                #             rotation=rep.distribution.uniform((0,0,0),(0,360,0))
                #         )
                #     # pass
                rep.orchestrator.run()

                return []