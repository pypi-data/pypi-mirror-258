#!/usr/bin/env python3

# Copyright 2015-2020 Earth Sciences Department, BSC-CNS

# This file is part of Autosubmit.

# Autosubmit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Autosubmit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with Autosubmit.  If not, see <http://www.gnu.org/licenses/>.

from autosubmit.platforms.wrappers.wrapper_builder import WrapperDirector, PythonVerticalWrapperBuilder, \
    PythonHorizontalWrapperBuilder, PythonHorizontalVerticalWrapperBuilder, PythonVerticalHorizontalWrapperBuilder, \
    BashHorizontalWrapperBuilder, BashVerticalWrapperBuilder, SrunHorizontalWrapperBuilder,SrunVerticalHorizontalWrapperBuilder


class WrapperFactory(object):

    def __init__(self, platform):
        self.as_conf = None
        self.platform = platform
        self.wrapper_director = WrapperDirector()
        self.exception = "This type of wrapper is not supported for this platform"

    def get_wrapper(self, wrapper_builder, **kwargs):
        wrapper_data = kwargs['wrapper_data']
        wrapper_data.wallclock = kwargs['wallclock']
        #todo here hetjobs
        if wrapper_data.het["HETSIZE"] <= 1:
            kwargs['allocated_nodes'] = self.allocated_nodes()
            kwargs['dependency'] = self.dependency(kwargs['dependency'])
            kwargs['partition'] = self.partition(wrapper_data.partition)
            kwargs["exclusive"] = self.exclusive(wrapper_data.exclusive)
            kwargs['nodes'] = self.nodes(wrapper_data.nodes)
            kwargs['tasks'] = self.tasks(wrapper_data.tasks)
            kwargs["custom_directives"] = self.custom_directives(wrapper_data.custom_directives)
            kwargs['queue'] = self.queue(wrapper_data.queue)
            kwargs['threads'] = self.threads(wrapper_data.threads)
            if str(kwargs['num_processors']).isdigit():
                kwargs['num_processors_value'] = int(wrapper_data.processors)
            else:
                kwargs['num_processors_value'] = 1
            if str(wrapper_data.nodes).isdigit() and int(wrapper_data.nodes) > 1 and kwargs['num_processors'] == '1':
                kwargs['num_processors'] = "#"
            else:
                kwargs['num_processors'] = self.processors(wrapper_data.processors)
        kwargs["executable"] = wrapper_data.executable

        kwargs['header_directive'] = self.header_directives(**kwargs)
        return self.wrapper_director.construct(wrapper_builder(**kwargs))

    def vertical_wrapper(self, **kwargs):
        raise NotImplemented(self.exception)

    def horizontal_wrapper(self, **kwargs):
        raise NotImplemented(self.exception)

    def hybrid_wrapper_horizontal_vertical(self, **kwargs):
        raise NotImplemented(self.exception)

    def hybrid_wrapper_vertical_horizontal(self, **kwargs):
        raise NotImplemented(self.exception)

    def header_directives(self, **kwargs):
        pass

    def allocated_nodes(self):
        return ''

    def dependency(self, dependency):
        return '#' if dependency is None else self.dependency_directive(dependency)
    def queue(self, queue):
        return '#' if not queue else self.queue_directive(queue)
    def processors(self, processors):
        return '#' if not processors or processors == "0" else self.processors_directive(processors)
    def nodes(self, nodes):
        return '#' if not nodes else self.nodes_directive(nodes)
    def tasks(self, tasks):
        return '#' if not tasks else self.tasks_directive(tasks)
    def partition(self, partition):
        return '#' if not partition else self.partition_directive(partition)
    def threads(self, threads):
        return '#' if not threads or threads in ["0","1"] else self.threads_directive(threads)
    def exclusive(self, exclusive):
        return '#' if not exclusive or str(exclusive).lower() == "false" else self.exclusive_directive(exclusive)
    def custom_directives(self, custom_directives):
        return '#' if not custom_directives else self.get_custom_directives(custom_directives)
    def get_custom_directives(self, custom_directives):
        """
        Returns custom directives for the specified job
        :param job: Job object
        :return: String with custom directives
        """
        # There is no custom directives, so directive is empty
        if custom_directives != '':
            return '\n'.join(str(s) for s in custom_directives)
        return ""

    def dependency_directive(self, dependency):
        raise NotImplemented(self.exception)
    def queue_directive(self, queue):
        raise NotImplemented(self.exception)
    def processors_directive(self, processors):
        raise NotImplemented(self.exception)
    def nodes_directive(self, nodes):
        raise NotImplemented(self.exception)
    def tasks_directive(self, tasks):
        raise NotImplemented(self.exception)
    def partition_directive(self, partition):
        raise NotImplemented(self.exception)
    def exclusive_directive(self, exclusive):
        raise NotImplemented(self.exception)
    def threads_directive(self, threads):
        raise NotImplemented(self.exception)

class SlurmWrapperFactory(WrapperFactory):

    def vertical_wrapper(self, **kwargs):
        return PythonVerticalWrapperBuilder(**kwargs)

    def horizontal_wrapper(self, **kwargs):

        if kwargs["method"] == 'srun':
            return SrunHorizontalWrapperBuilder(**kwargs)
        else:
            return PythonHorizontalWrapperBuilder(**kwargs)

    def hybrid_wrapper_horizontal_vertical(self, **kwargs):
        return PythonHorizontalVerticalWrapperBuilder(**kwargs)

    def hybrid_wrapper_vertical_horizontal(self, **kwargs):
        if kwargs["method"] == 'srun':
            return SrunVerticalHorizontalWrapperBuilder(**kwargs)
        else:
            return PythonVerticalHorizontalWrapperBuilder(**kwargs)

    def header_directives(self, **kwargs):
        return self.platform.wrapper_header(**kwargs)

    def allocated_nodes(self):
        return self.platform.allocated_nodes()

    def dependency_directive(self, dependency):
        return '#SBATCH --dependency=afterok:{0}'.format(dependency)
    def queue_directive(self, queue):
        return '#SBATCH --qos={0}'.format(queue)
    def partition_directive(self, partition):
        return '#SBATCH --partition={0}'.format(partition)
    def exclusive_directive(self, exclusive):
        return '#SBATCH --exclusive'
    def tasks_directive(self, tasks):
        return '#SBATCH --ntasks-per-node={0}'.format(tasks)
    def nodes_directive(self, nodes):
        return '#SBATCH -N {0}'.format(nodes)
    def processors_directive(self, processors):
        return '#SBATCH -n {0}'.format(processors)
    def threads_directive(self, threads):
        return '#SBATCH --cpus-per-task={0}'.format(threads)



class LSFWrapperFactory(WrapperFactory):

    def vertical_wrapper(self, **kwargs):
        return PythonVerticalWrapperBuilder(**kwargs)

    def horizontal_wrapper(self, **kwargs):
        return PythonHorizontalWrapperBuilder(**kwargs)

    def header_directives(self, **kwargs):
        return self.platform.wrapper_header(**kwargs)

    def queue_directive(self, queue):
        return queue

    def dependency_directive(self, dependency):
        return '#BSUB -w \'done({0})\' [-ti]'.format(dependency)


class EcWrapperFactory(WrapperFactory):

    def vertical_wrapper(self, **kwargs):
        return BashVerticalWrapperBuilder(**kwargs)

    def horizontal_wrapper(self, **kwargs):
        return BashHorizontalWrapperBuilder(**kwargs)

    def header_directives(self, **kwargs):
        return self.platform.wrapper_header(**kwargs)

    def queue_directive(self, queue):
        return queue

    def dependency_directive(self, dependency):
        return '#PBS -v depend=afterok:{0}'.format(dependency)

class PJMWrapperFactory(WrapperFactory):

    def vertical_wrapper(self, **kwargs):
        return PythonVerticalWrapperBuilder(**kwargs)

    def horizontal_wrapper(self, **kwargs):

        if kwargs["method"] == 'srun':
            return SrunHorizontalWrapperBuilder(**kwargs)
        else:
            return PythonHorizontalWrapperBuilder(**kwargs)

    def hybrid_wrapper_horizontal_vertical(self, **kwargs):
        return PythonHorizontalVerticalWrapperBuilder(**kwargs)

    def hybrid_wrapper_vertical_horizontal(self, **kwargs):
        if kwargs["method"] == 'srun':
            return SrunVerticalHorizontalWrapperBuilder(**kwargs)
        else:
            return PythonVerticalHorizontalWrapperBuilder(**kwargs)

    def header_directives(self, **kwargs):
        return self.platform.wrapper_header(**kwargs)

    def allocated_nodes(self):
        return self.platform.allocated_nodes()

    #def dependency_directive(self, dependency):
    #    # There is no option for afterok in the PJM scheduler, but I think it is not needed.
    #    return '#PJM --dependency=afterok:{0}'.format(dependency)

    def queue_directive(self, queue):
        return '#PJM -L rscgrp={0}'.format(queue)

    def partition_directive(self, partition):
        return '#PJM -g {0}'.format(partition)
