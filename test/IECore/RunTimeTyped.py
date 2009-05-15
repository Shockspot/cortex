##########################################################################
#
#  Copyright (c) 2007-2009, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#
#     * Neither the name of Image Engine Design nor the names of any
#       other contributors to this software may be used to endorse or
#       promote products derived from this software without specific prior
#       written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import unittest
import IECore

class TestRunTimeTyped( unittest.TestCase ) :

	def test( self ) :

		i = IECore.IntData( 10 )
		self.assert_( i.isInstanceOf( "IntData" ) )
		self.assert_( i.isInstanceOf( "Data" ) )
		self.assert_( i.isInstanceOf( "Object" ) )
		self.assert_( i.isInstanceOf( "RunTimeTyped" ) )

		self.assert_( i.isInstanceOf( IECore.TypeId.IntData ) )
		self.assert_( i.isInstanceOf( IECore.TypeId.Data ) )
		self.assert_( i.isInstanceOf( IECore.TypeId.Object ) )
		self.assert_( i.isInstanceOf( IECore.TypeId.RunTimeTyped ) )

		self.assertEqual( i.baseTypeId(), IECore.TypeId.Data )

		self.assert_( IECore.IntData.inheritsFrom( "Data" ) )
		self.assert_( IECore.IntData.inheritsFrom( "Object" ) )
		self.assert_( IECore.IntData.inheritsFrom( "RunTimeTyped" ) )

		self.assert_( IECore.IntData.inheritsFrom( IECore.TypeId.Data ) )
		self.assert_( IECore.IntData.inheritsFrom( IECore.TypeId.Object ) )
		self.assert_( IECore.IntData.inheritsFrom( IECore.TypeId.RunTimeTyped ) )

		self.assert_( IECore.Data.inheritsFrom( IECore.TypeId.Object ) )
		self.assert_( IECore.Data.inheritsFrom( IECore.TypeId.RunTimeTyped ) )

		self.assert_( IECore.Object.inheritsFrom( IECore.TypeId.RunTimeTyped ) )

		self.assertEqual( IECore.RunTimeTyped.typeNameFromTypeId( IECore.TypeId.IntData ), "IntData" )
		self.assertEqual( IECore.RunTimeTyped.typeIdFromTypeName( "IntData" ), IECore.TypeId.IntData )

	def testStaticTypeBindings( self ) :

		import IECore

		typeNames={}
		typeIds = {}

		# Make that all classes derived from RunTimeTyped correctly bind staticTypeName and staticTypeId
		for typeName in dir(IECore):

			t = getattr(IECore, typeName)

			baseClasses = []

			# Iteratively expand base classes all the way to the top
			if hasattr(t, "__bases__"):
				baseClasses = list( t.__bases__ )

				i=0
				while i < len(baseClasses):
					for x in baseClasses[i].__bases__:
						baseClasses.extend([x])

					i = i + 1

			if IECore.RunTimeTyped in baseClasses:

				baseIds = IECore.RunTimeTyped.baseTypeIds( t.staticTypeId() )
				baseIds = set( [ int(x) for x in baseIds ] )

				self.assert_( hasattr(t, "staticTypeName") )
				self.assert_( hasattr(t, "staticTypeId") )
				self.assert_( hasattr(t, "baseTypeId") )
				self.assert_( hasattr(t, "baseTypeName") )

				self.assert_( t.staticTypeId() in IECore.TypeId.values.keys() )

				# Make sure that no 2 IECore classes provide the same typeId or typeName
				if t.staticTypeName() in typeNames:
					raise RuntimeError( "'%s' does not have a unique RunTimeTyped static type name (conflicts with '%s')." % ( t.__name__ , typeNames[t.staticTypeName()] ))

				if t.staticTypeId() in typeIds:
					raise RuntimeError( "'%s' does not have a unique RunTimeTyped static type id (conflicts with '%s')." % (t.__name__ , typeIds[t.staticTypeId()] ))

				self.assertEqual( IECore.RunTimeTyped.typeNameFromTypeId( t.staticTypeId() ), t.staticTypeName() )
				self.assertEqual( IECore.RunTimeTyped.typeIdFromTypeName( t.staticTypeName() ), t.staticTypeId() )

				for base in baseClasses :

					if issubclass( base, IECore.RunTimeTyped ) :

						self.assertNotEqual( base.staticTypeId(), t.staticTypeId() )
						if not base.staticTypeId() in IECore.RunTimeTyped.baseTypeIds( t.staticTypeId() ):
							raise Exception( "'%s' does not have '%s' in its RunTimeTyped base classes, even though Python says it derives from it." % (t.staticTypeName(), base.staticTypeName() ))

				typeNames[t.staticTypeName()] = t.__name__
				typeIds[t.staticTypeId()] = t.__name__


	def testRegisterRunTimeTyped( self ) :

		# should raise because 100009 is already been registered as OptionalCompoundParameter
		self.assertRaises( RuntimeError, IECore.registerRunTimeTyped, IECore.FileSequenceParameter, 100009, IECore.PathParameter )

		self.assertEqual( IECore.TypeId.FileSequenceParameter, IECore.FileSequenceParameter.staticTypeId() )
		self.assertEqual( IECore.TypeId.FileSequenceParameter, IECore.FileSequenceParameter( "", "" ).typeId() )

		self.assert_( IECore.FileSequenceParameter.inheritsFrom( "PathParameter" ) )
		self.assert_( IECore.FileSequenceParameter.inheritsFrom( IECore.TypeId.PathParameter ) )
		self.assert_( IECore.FileSequenceParameter.inheritsFrom( "StringParameter" ) )
		self.assert_( IECore.FileSequenceParameter.inheritsFrom( IECore.TypeId.StringParameter ) )
		self.assert_( IECore.FileSequenceParameter.inheritsFrom( "Parameter" ) )
		self.assert_( IECore.FileSequenceParameter.inheritsFrom( IECore.TypeId.Parameter ) )
		self.assert_( IECore.FileSequenceParameter.inheritsFrom( "RunTimeTyped" ) )
		self.assert_( IECore.FileSequenceParameter.inheritsFrom( IECore.TypeId.RunTimeTyped ) )

		self.assert_( IECore.FileSequenceParameter( "", "" ).isInstanceOf( "FileSequenceParameter" ) )
		self.assert_( IECore.FileSequenceParameter( "", "" ).isInstanceOf( IECore.TypeId.FileSequenceParameter ) )
		self.assert_( IECore.FileSequenceParameter( "", "" ).isInstanceOf( "PathParameter" ) )
		self.assert_( IECore.FileSequenceParameter( "", "" ).isInstanceOf( IECore.TypeId.PathParameter ) )
		self.assertRaises( TypeError, IECore.FileSequenceParameter( "", "" ).isInstanceOf, 10 )



if __name__ == "__main__":
    unittest.main()
