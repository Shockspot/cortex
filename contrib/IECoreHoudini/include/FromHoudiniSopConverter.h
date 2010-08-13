//////////////////////////////////////////////////////////////////////////
//
//  Copyright 2010 Dr D Studios Pty Limited (ACN 127 184 954) (Dr. D Studios),
//  its affiliates and/or its licensors.
//
//  Copyright (c) 2010, Image Engine Design Inc. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//
//     * Redistributions of source code must retain the above copyright
//       notice, this list of conditions and the following disclaimer.
//
//     * Redistributions in binary form must reproduce the above copyright
//       notice, this list of conditions and the following disclaimer in the
//       documentation and/or other materials provided with the distribution.
//
//     * Neither the name of Image Engine Design nor the names of any
//       other contributors to this software may be used to endorse or
//       promote products derived from this software without specific prior
//       written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//////////////////////////////////////////////////////////////////////////

#ifndef IE_COREHOUDINI_FROMHOUDINISOPCONVERTER_H
#define IE_COREHOUDINI_FROMHOUDINISOPCONVERTER_H

// Houdini
#include <GU/GU_Detail.h>
#include <SOP/SOP_Node.h>
#include <UT/UT_Version.h>

// Cortex
#include <IECore/MeshPrimitive.h>
#include <IECore/PointsPrimitive.h>

// IECoreHoudini
#include "TypeIds.h"
#include "FromHoudiniNodeConverter.h"

namespace IECoreHoudini
{
	
	/// Utility class for storing attribute information
	struct AttributeInfo
	{
		public:
			friend class FromHoudiniSopConverter;

		private:
			std::string name;
			IECore::DataPtr data;
			IECore::PrimitiveVariable::Interpolation interp;
			int entries;
			GB_AttribType type;
#if UT_MAJOR_VERSION_INT >= 11
			GB_AttributeRef offset;
#else
			int offset;
#endif
	};

	/// Converter which converts from Houdini SOP geometry to Cortex Mesh/Points primitive
	class FromHoudiniSopConverter : public IECoreHoudini::FromHoudiniNodeConverter
	{
		public :
			
			IE_CORE_DECLARERUNTIMETYPEDEXTENSION( FromHoudiniSopConverter, FromHoudiniSopConverterTypeId, IECore::ToCoreConverter );
			
			typedef SOP_Node FromType;
			
			FromHoudiniSopConverter( const SOP_Node *sop );
			
			virtual ~FromHoudiniSopConverter();

			/// performs our conversion to a Cortex primitive
			virtual IECore::ObjectPtr doConversion( IECore::ConstCompoundObjectPtr operands ) const;

			/// retrieves the SOP_Node held by the converter
			SOP_Node *sop() const;

		private :
			
			/// gathers attribute information and allocates storage
			void getAttribInfo( const GU_Detail *geo, const UT_LinkList *attribs, IECore::PrimitiveVariable::Interpolation interp_type, std::vector<AttributeInfo> &info, int num_entries ) const;

			/// extracts point attributes
			void extractPointAttribs( const GU_Detail *geo, const GEO_PointList &points, std::vector<AttributeInfo> &info ) const;

			/// extracts detail attributes
			void extractDetailAttribs( const GU_Detail *geo, std::vector<AttributeInfo> &info ) const;

			/// extracts primitive/vertex attributes
			void extractPrimVertAttribs( const GU_Detail *geo, const GEO_PrimList &pprim, std::vector<AttributeInfo> &info ) const;

			static FromHoudiniNodeConverter::Description<FromHoudiniSopConverter> m_description;
	};

// register our converter
IE_CORE_DECLAREPTR( FromHoudiniSopConverter );

}

#endif // IE_COREHOUDINI_FROMHOUDINISOPCONVERTER_H
